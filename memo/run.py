import sys
import datetime
import argparse
import textwrap
import locale
import subprocess

from .ansi import term
from .config import Config, make_memo_config
from .core import Memo

LOGAPPNAME = 'simple memo tool'


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

    subparsers = parser.add_subparsers(dest='subparser_name', help='sub memo command')

    parser_new = subparsers.add_parser('new', help='open new file')
    parser_new.add_argument('-e', '--extension',
                            nargs='?',
                            default='rst',
                            help='set memo file extension')

    parser_grep = subparsers.add_parser('grep', help='grep memo files')
    parser_grep.add_argument('pattern', help='grep pattern')

    subparsers.add_parser('list', help='show memo files')

    subparsers.add_parser('init', help='init memo')

    return parser


def get_locale():
    locale.setlocale(locale.LC_ALL, '')
    output_encoding = locale.getpreferredencoding()
    return output_encoding


def main():
    parser = get_argparser()
    args = parser.parse_args()
    if args.subparser_name == 'init':
        make_memo_config()
    elif args.subparser_name == 'new':
        config = Config()
        filename = input('filename: ')
        now = datetime.datetime.now()
        formated = '{}/{:%Y-%m-%d}_{}.{}'.format(config.memodir,
                                                 now,
                                                 filename,
                                                 args.extension)
        subprocess.run([config.editor, formated])
    elif args.subparser_name == 'list':
        config = Config()
        encoding = get_locale()
        with Memo(config.memodir, encoding) as memo:
            exit_code = memo.loop()
        sys.exit(exit_code)
    elif args.subparser_name == 'grep':
        config = Config()
        encoding = get_locale()
        with Memo(config.memodir, encoding, pattern=args.pattern) as memo:
            memo.grep()
            exit_code = memo.loop()
        sys.exit(exit_code)
