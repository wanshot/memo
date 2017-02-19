import sys
import datetime
import argparse
import textwrap
import locale
import subprocess

from .ansi import term
from .config import Config, make_memo_config
from .core import Memo

LOGAPPNAME = 'memo'


def get_argparser():
    from memo import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='memo',
        description=textwrap.dedent(
            term(LOGAPPNAME, {'fg_color': 'red'}) + '\n' +
            term(__logo__, {'fg_color': 'red', 'style': 'bold'})
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-v', '--version',
                        action='version',
                        version='{version}'.format(version=__version__))

    parser.add_argument('filename',
                        nargs='?',
                        type=str)

    parser.add_argument('-l', '--list',
                        action='store_true',
                        default=False,
                        help='show memo list')

    parser.add_argument('-i', '--init',
                        action='store_true',
                        default=False,
                        help='init memo')
    return parser


def get_locale():
    locale.setlocale(locale.LC_ALL, '')
    output_encoding = locale.getpreferredencoding()
    return output_encoding


def main():
    parser = get_argparser()
    args = parser.parse_args()
    if args.init:
        make_memo_config()
    elif args.filename:
        config = Config()
        now = datetime.datetime.now()
        formated = '{}/{:%Y-%m-%d}_{}.rst'.format(config.memodir,
                                                  now,
                                                  args.filename)
        subprocess.run([config.editor, formated])
    elif args.list:
        config = Config()
        encoding = get_locale()
        with Memo(config.memodir, encoding) as memo:
            exit_code = memo.choice_file()
        sys.exit(exit_code)
