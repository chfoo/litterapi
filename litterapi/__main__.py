import argparse
import json
import sys
import time

from litterapi.api import SearchAPI


def main():
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers()

    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('query')
    search_parser.add_argument('--wait', type=float, default=1)
    search_parser.set_defaults(func=search_command)

    args = arg_parser.parse_args()

    if not hasattr(args, 'func'):
        arg_parser.print_usage()
        sys.exit(2)

    return args.func(args)


def search_command(args):
    api = SearchAPI(args.query)

    while True:
        results = api.fetch()

        if not results:
            break

        for result in results:
            print(json.dumps(result))

        time.sleep(args.wait)


if __name__ == '__main__':
    main()
