import argparse
import os
import sys
import pytest
from airobots import __description__, __version__
from airhttprunner.cli import main_run
from airtest.core.settings import Settings as ST


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    parser.add_argument(
        "-t", "--type", dest="test type", required=True, default='api', choices=['api', 'web', 'ios', 'android'], help="test type, choices: api, web, ios, android"
    )
    parser.add_argument(
        "-b", "--browser", dest="test browser", default='Chrome', choices=['Firefox', 'Chrome', 'Ie', 'Opera', 'Safari', 'PhantomJS'], help="test browser, choices: Firefox, Chrome, Ie, Opera, Safari, PhantomJS"
    )
    parser.add_argument(
        "-r", "--remote-url", dest="remote url", default=None, help="web test's remote url, eg. http://localhost:4444/wd/hub"
    )
    
    if len(sys.argv) == 1:
        # httprunner
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) in (2, 3, 4) and sys.argv[1] not in ["-t", "--type", "-b", "--browser", "-r", "--remote-url"]:
        if sys.argv[1] in ["-v", "--version"]:
            print(f"{__version__}")
        else:
            parser.print_help()
        sys.exit(0)
    elif (
        len(sys.argv) in (5, 6) and (sys.argv[1] not in ["-t", "--type", "-b", "--browser", "-r", "--remote-url"] and sys.argv[3] not in ["-t", "--type", "-b", "--browser", "-r", "--remote-url"])
    ):
        if sys.argv[1] in ["-v", "--version"]:
            print(f"{__version__}")
        else:
            parser.print_help()
        sys.exit(0)
        
    extra_args = []
    if len(sys.argv) >= 2:
        args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    args_parames = args.__dict__

    ST.BROWSER = 'Chrome'
    ST.REMOTE_URL = None
    if args_parames.get('test type') == "api":
        sys.exit(main_run(extra_args))
    elif args_parames.get('test type') in ['web', 'ios', 'android']:
        ST.BROWSER = args_parames.get('test browser', ST.BROWSER)
        ST.REMOTE_URL = args_parames.get('remote url', ST.REMOTE_URL)
        ST.LOG_DIR = 'logs'
        if not os.path.exists(ST.LOG_DIR): os.makedirs(ST.LOG_DIR)
        sys.exit(pytest.main(extra_args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()