import requests
from datetime import datetime
from bs4 import BeautifulSoup
from .excel import ExcelWriter
import os
import shutil
import pickle


class AUser:
    def __init__(self, id_, name, rank, rating):
        self.id, self.name, self.rank, self.rating, self.send = id_, name, rank, rating, None

    @staticmethod
    def sort_function(user):
        return user.rank

    def writable(self):
        return 'ID: {}\nБаллы: {}\nМесто: {}\nПосылок: {}\n'.format(self.id, self.rating, self.rank, self.send)

    def writable_md(self):
        return '| {} | {} | {} | {} | {} |'.format(self.id, self.name, self.rank, self.rating, self.send)

    def writable_txt(self):
        return '{}\t{}{}\t{}\t{}'.format(self.id, self.name + ' ' * max(0, 25 - len(self.name)), self.rank, self.rating,
                                         self.send)


class ATask:
    def __init__(self, id_, good, bad, lang_translate):
        self.id, self.good, self.bad = id_, good, bad
        self.good_langs, self.bad_langs = {}, {}
        self.lang_translate = lang_translate

    def status(self):
        return self.good > 0

    def solve(self, lang):
        if lang in self.lang_translate:
            lang = self.lang_translate[lang]
        self.good += 1
        if lang not in self.good_langs:
            self.good_langs[lang] = 0
        self.good_langs[lang] += 1

    def solved(self, langs=None):
        if langs is None:
            return self.good
        return sum(self.good_langs[lang] if lang in self.good_langs else 0 for lang in langs)

    def unsolve(self, lang):
        if lang in self.lang_translate:
            lang = self.lang_translate[lang]
        self.bad += 1
        if lang not in self.bad_langs:
            self.bad_langs[lang] = 0
        self.bad_langs[lang] += 1

    def unsolved(self, langs=None):
        if langs is None:
            return self.bad
        return sum(self.bad_langs[lang] if lang in self.bad_langs else 0 for lang in langs)

    @staticmethod
    def sort_function(task):
        return task.id

    def pm(self, lang=None):
        result, good, bad = '', self.solved(lang), self.unsolved(lang)
        if good > 0:
            result += '{}+'.format(good)
            if bad > 0:
                result += ', '
        if bad > 0:
            result += '{}-'.format(bad)
        return result

    def __repr__(self):
        return '{} ({})'.format(self.id, self.pm())


class ATasks:
    def __init__(self, bad_with_lang, good_with_lang, lang_translate):
        self.lang_translate = lang_translate
        bad, good = [_[0] for _ in bad_with_lang], [_[0] for _ in good_with_lang]
        self.map_tasks = {_: ATask(_, 0, 0, lang_translate) for _ in set(bad).union(good)}
        self.max_task = 0
        for task in good_with_lang:
            self.map_tasks[task[0]].solve(task[1])
        for task in bad_with_lang:
            self.map_tasks[task[0]].unsolve(task[1])
        self.good, self.bad, self.goods, self.bads = 0, 0, 0, 0
        self.tasks = self.map_tasks.values()
        for task in self.tasks:
            self.max_task = max(self.max_task, task.id)
            if task.id <= 1000:
                if task.status():
                    self.goods += 1
                else:
                    self.bads += 1
            else:
                if task.status():
                    self.good += 1
                else:
                    self.bad += 1

    def get_task(self, task):
        if task not in self.map_tasks:
            return ATask(task, 0, 0, self.lang_translate)
        return self.map_tasks[task]

    def writable(self, last_solve):
        result = 'Всего решено {}, из них в первой тысяче {}\n'.format(self.good + self.goods, self.goods)
        result += 'Всего не решено {}, из них в первой тысяче {}\n'.format(self.bad + self.bads, self.bads)
        result += 'Последняя попытка: {}\n'.format(last_solve)
        tasks = {}
        for task in self.tasks:
            part = (task.id - 1) // 100
            if part not in tasks:
                tasks[part] = [[], []]
            if task.status():
                tasks[part][0].append(task)
            else:
                tasks[part][1].append(task)
        tasks = sorted(tasks.items(), key=lambda x: x[0])
        for part in tasks:
            p, t = part
            result += '\nЗадачи {} — {}:\n'.format(p * 100 + 1, p * 100 + 100)
            good = sorted(t[0], key=ATask.sort_function)
            bad = sorted(t[1], key=ATask.sort_function)
            result += 'Решено ({}): {}\n'.format(len(good), str(good)[1:-1])
            result += 'Не решено ({}): {}\n'.format(len(bad), str(bad)[1:-1])
        return result

    def writable_md(self):
        return ' {} | {} | {} | {} |\n'.format(self.goods, self.bads, self.goods + self.good, self.bads + self.bad)

    def writable_txt(self):
        return '\t{}\t   {}\t\t{}\t{}\n'.format(self.goods, self.bads, self.goods + self.good, self.bads + self.bad)


def parse_user_profile(user_id):
    url = 'https://acmp.ru/?main=user&id='
    r = requests.get(url + str(user_id))
    html_parser = BeautifulSoup(r.text, 'html.parser')
    rank = html_parser.find_all('b', {'class': 'btext'})[0]
    rank = int(rank.text.split()[1])
    rating = html_parser.find_all('b', {'class': 'btext'})[1]
    rating = int(rating.text.split()[1])
    user_name = html_parser.find_all('td', {'class': 'menu_title'})[4].text
    user_name = bytes(user_name, r.encoding).decode('cp1251').title()
    user_name = ' '.join(user_name.split(' ')[0:2])
    return AUser(user_id, user_name, rank, rating)


def load_saved(raw_file):
    if not os.path.exists(raw_file):
        return [], [], -1
    with open(raw_file, 'rb') as f:
        data = pickle.load(f)
    return data


def dump_saved(raw_file, *args):
    with open(raw_file, 'wb') as f:
        pickle.dump(args, f)


def parse_user_submissions(user_id, raw_file, lang_translate):
    bad_task, good_task, last_solve = load_saved(raw_file)
    first_solve = last_solve
    page = 0
    while True:
        print('Page', page)
        url = 'https://acmp.ru/index.asp?main=status&id_mem={0}&id_res=0&id_t=0&page={1}&uid=0'.format(user_id, page)
        r = requests.get(url + str(user_id))
        html_parser = BeautifulSoup(r.text, 'html.parser')
        rows = html_parser.find_all('table', {'class': 'main refresh'})[0].findAll('tr')
        for row in rows:
            id_, tim, user, task, lang, res, test, etime, emem = (_.text for _ in row.findAll('td'))
            if first_solve == last_solve:
                first_solve = id_
            if id_ == last_solve:
                rows = []
                break
            task = int(task)
            if res == 'Accepted':
                good_task.append([task, lang])
            else:
                bad_task.append([task, lang])
        if len(rows) < 20:
            break
        page += 1
    dump_saved(raw_file, bad_task, good_task, first_solve)
    return ATasks(bad_task, good_task, lang_translate), len(good_task) + len(bad_task), first_solve


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def writable_md(time, data):
    result = '''# Результаты acmp
Здесь можно увидеть результаты решения задач на сайте [acmp](https://acmp.ru). 

## Результаты
Все решенные задачи можно увидеть в `results.xlsx`.  
Результаты всей группы можно увидеть ниже и в `results.txt`.  
Свои результаты можно посмотреть в папке `users_results`.  
Домашняя работа написана в папке `tasks`, а её выполнение в папке `tasks_results`.

## Таблица
Время обновления: {}
| ID   | Участник | Место | Рейтинг | Посылки | + (1000) | - (1000) | +    | -    |
| ---- | -------- | ----- | ------- | ------- | -------- | -------- | ---- | ---- |
'''.format(time)
    for x in data:
        result += x[0].writable_md() + x[1].writable_md()
    return result


def writable_md_task(time, data, task):
    result = '''# Задачи {}
Время обновления: {}
| ID   | Участник | +    | -    |
| ---- | -------- | ---- | ---- |
'''.format(task, time)
    for i in range(1, len(data[0])):
        result += '| {} | {} | {} | {} |\n'.format(data[1][i], data[0][i], data[2][i], data[3][i])
    return result


def writable_txt(time, data):
    result = '''Время обновления: {}
ID	Участник                 Место	Рейтинг	Посылки	+ (1000)   - (1000)	+	-
'''.format(time)
    for x in data:
        result += x[0].writable_txt() + x[1].writable_txt()
    return result


def parse_group(cache_folder, group_folder, users, lang_translate):
    cache_raw_folder, cache_res_folder = cache_folder + 'raw/', cache_folder + 'user/'
    res_folder, tasks_folder = group_folder + 'users_results/', group_folder + 'tasks_results/'
    if os.path.exists(res_folder):
        shutil.rmtree(res_folder)
    if os.path.exists(tasks_folder):
        shutil.rmtree(tasks_folder)
    os.makedirs(res_folder)
    os.makedirs(tasks_folder)
    result, parsing_time = [], get_time()
    for now in users:
        user = parse_user_profile(now)
        tasks, user.send, last_solve = parse_user_submissions(now, cache_raw_folder + str(user.id) + '.txt',
                                                              lang_translate)
        with open(res_folder + user.name + ' (' + str(user.id) + ').txt', 'w', encoding='utf-8') as f:
            f.write(user.writable())
            f.write(tasks.writable(last_solve))
        with open(cache_res_folder + str(user.id) + '.txt', 'w', encoding='utf-8') as f:
            f.write(user.writable())
            f.write(tasks.writable(last_solve))
        result.append([user, tasks])
    result = sorted(result, key=lambda x: x[0].rank)
    ExcelWriter().write(group_folder + 'results.xlsx', result)
    with open(group_folder + 'results.md', 'w', encoding='utf-8') as f:
        f.write(writable_md(parsing_time, result))
    with open(group_folder + 'results.txt', 'w', encoding='utf-8') as f:
        f.write(writable_txt(parsing_time, result))
    for tasks_file in os.listdir(group_folder + 'tasks'):
        langs, tasks = [], []
        with open(group_folder + 'tasks/' + tasks_file) as f:
            for line in f.read().split('\n'):
                if not line:
                    continue
                if line.isdigit():
                    tasks.append(int(line))
                else:
                    langs.extend(line.split('|'))
            tasks = sorted(tasks)
        task_full_name = tasks_folder + tasks_file.rsplit('.', 1)[0]
        data = ExcelWriter().write(task_full_name + '.xlsx', result, tasks, langs)
        with open(task_full_name + '.md', 'w', encoding='utf-8') as f:
            f.write(writable_md_task(parsing_time, data, tasks_file.rsplit('.', 1)[0]))
