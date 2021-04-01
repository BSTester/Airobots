import argparse
import os
import sys
import pytest
from airobots import __description__, __version__
from airhttprunner.cli import main_run
from .core.settings import ST


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    parser.add_argument(
        "-t", "--type", dest="type", required=True, default='api', choices=['api', 'web', 'ios', 'android'], help="test type, choices: api, web, ios, android"
    )
    parser.add_argument(
        "-b", "--browser", dest="browser", default='Chrome', choices=['Firefox', 'Chrome', 'Ie', 'Opera', 'Safari', 'PhantomJS'], help="test browser, choices: Firefox, Chrome, Ie, Opera, Safari, PhantomJS"
    )
    parser.add_argument(
        "-r", "--remote-url", dest="remote_url", default=None, help="gui test's remote url, eg. http://localhost:4444/wd/hub"
    )
    
    if len(sys.argv) < 2:
        # httprunner
        parser.print_help()
        sys.exit(0)

    extra_args = []
    if len(sys.argv) >= 2:
        if sys.argv[1] in ["-v", "--version"]:
            print(f"{__version__}")
            sys.exit(0)
        elif sys.argv[1] in ["-h", "--help"]:
            parser.print_help()
            sys.exit(0)
        else:
            args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if args.type == "api":
        sys.exit(main_run(extra_args))
    elif args.type in ['web', 'ios', 'android']:
        ST.BROWSER = args.browser or ST.BROWSER
        ST.REMOTE_URL = args.remote_url or ST.REMOTE_URL
        ST.PLATFORM_NAME = args.type or ST.PLATFORM_NAME
        if not os.path.exists(ST.LOG_DIR): os.makedirs(ST.LOG_DIR)
        sys.exit(pytest.main(extra_args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()