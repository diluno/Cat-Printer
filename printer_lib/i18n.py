'Minimal internationalization lib'

import os
import json
import locale

class I18nLib():
    ''' Minimal implementation of current frontend i18n in Python.
        Not Complete (yet)!
    '''

    lang: str
    fallback: str
    data: dict = {}

    def __init__(self, search_path='lang', lang=None, fallback=None):
        # self.lang = lang or locale.getdefaultlocale()[0].replace('_', '-')
        self.lang = 'en-US'
        self.fallback = fallback or 'en-US'
        with open(os.path.join(search_path, self.fallback + '.json'),
                  'r', encoding='utf-8') as file:
            self.data = json.load(file)
        path = self.lang + '.json'
        if path in os.listdir(search_path):
            with open(os.path.join(search_path, path), 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key in data:
                    self.data[key] = data[key]

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys, )
        string = self.data.get(keys[0], keys[0])
        if len(keys) > 1:
            if isinstance(keys[-1], dict):
                string = string.format(*keys[1:-1], **keys[-1])
            else:
                string = string.format(*keys[1:])
        return string
