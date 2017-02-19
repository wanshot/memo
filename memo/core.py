import os
import sys
import termios
import tty
import subprocess
import glob
from collections import OrderedDict

from wcwidth import wcwidth

from .ansi import term
from .terminalsize import get_terminal_size
from .config import Config


class Memo(object):

    def __init__(self, memodir, output_encodeing, input_encoding='utf-8', kwargs=None):
        self.width, self.height = get_terminal_size()
        self.file2path = self.get_memodir_files(memodir)
        self.file_count = len(self.file2path.keys())
        self.output_encodeing = output_encodeing
        self.input_encoding = input_encoding

    def __enter__(self):
        self.pos = 1
        self.finished = False
        self.filename = None
        self.config = Config()
        ttyname = get_ttyname()
        sys.stdin = open(ttyname)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write('\x1b[?25h\x1b[0J')
        if self.finished:
            pass
        elif self.filename:
            subprocess.call([self.config.editor, self.filename])

    def choice_file(self):
        self.render()
        while True:
            try:
                ch = get_char()

                if ch in self.config.get_key('QUITE'):
                    self.finished = True
                    break
                elif ch in self.config.get_key('UP'):
                    if self.pos > 1:
                        self.pos -= 1
                elif ch in self.config.get_key('DOWN'):
                    if self.pos < self.file_count:
                        self.pos += 1
                elif ch == '\n':
                    self.filename = self.file2path[list(self.file2path.keys())[self.pos - 1]]
                    break
                self.render()
            except:
                sys.stdout.write('\x1b[?0h\x1b[0J')
        return 1

    def render(self):
        reset = '\x1b[0K\x1b[0m'
        sys.stdout.write('\x1b[?25l')  # hide cursor

        for idx, filename in enumerate(self.file2path.keys(), start=1):
            sys.stdout.write('\x1b[0K')
            eol = '' if self.file_count == idx else '\n'

            if idx == self.pos:
                sys.stdout.write(
                    term(self.truncate_string_by_line(filename),
                         self.config.select_line_attribute,
                         ) + eol + reset + '\r')
            else:
                sys.stdout.write(
                    term(self.truncate_string_by_line(filename),
                         self.config.normal_line_attribute,
                         ) + eol + reset + '\r')

        sys.stdout.write('\x1b[{}A'.format(self.file_count - 1))

    def truncate_string_by_line(self, line):
        counter = 0
        string = []
        for s in line:
            counter += wcwidth(s)
            if counter > self.width:
                break
            else:
                string.append(s)
        return ''.join(string)

    def get_memodir_files(self, memodir):
        name2path = OrderedDict()
        for ap in glob.glob('{}/*'.format(memodir)):
            name2path[ap.split('/')[-1]] = ap
        return name2path


def get_ttyname():
    for file_obj in (sys.stdin, sys.stdout, sys.stderr):
        if file_obj.isatty():
            return os.ttyname(file_obj.fileno())


def get_char():
    try:
        from msvcrt import getch
        return getch()
    except ImportError:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
