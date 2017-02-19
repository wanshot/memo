import os
from configparser import ConfigParser

HOME = os.path.expanduser('~')
MEMO_CONF_DIRECTORY = os.path.join(HOME, '.memo.d')
MEMO_CONF_PATH = os.path.join(MEMO_CONF_DIRECTORY, 'memorc')

DEFAULT_CONFIG = """
[base]
EDITOR =
MEMODIR =
SHELL =

[normal line attribute]
FG_COLOR = white
BG_COLOR = black
STYLE =
[select line attribute]
FG_COLOR = yellow
BG_COLOR = red
STYLE = bold

[keymap]
UP = k
DOWN = j
QUITE = q, ESC
ENTER = ENTER
"""

KEY_MAP = {
    'ESC': '\x1b'
}


def make_memo_config():
    if not os.path.exists(MEMO_CONF_DIRECTORY):
        os.makedirs(MEMO_CONF_DIRECTORY)
    with open(MEMO_CONF_PATH, 'w+') as f:
        f.write(DEFAULT_CONFIG)


class Config(object):

    def __init__(self):
        if not os.path.exists(MEMO_CONF_DIRECTORY):
            exit('No such .memo.d')
        if not os.path.isfile(MEMO_CONF_PATH):
            exit('No such memorc')

        self.config = ConfigParser()
        self.config.read(MEMO_CONF_PATH)

    def get_key(self, key):
        keys = []
        for key in self.config['keymap'][key].replace(' ', '').split(','):
            if KEY_MAP.get(key):
                keys.append(KEY_MAP[key])
            else:
                keys.append(key)
        return keys

    @property
    def memodir(self):
        return self.config.get('base', 'MEMODIR')

    @property
    def editor(self):
        if self.config.get('base', 'EDITOR'):
            return self.config.get('base', 'EDITOR')
        else:
            return os.environ.get('EDITOR', 'vim')

    @property
    def shell(self):
        return self.config.get('base', 'SHELL')

    @property
    def normal_line_attribute(self):
        return self.config['normal line attribute']

    @property
    def select_line_attribute(self):
        return self.config['select line attribute']
