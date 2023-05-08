import argparse

from lib.web import start_server
from lib.helpers import fill_db, schedule_task


def parse_args():
    parser = argparse.ArgumentParser(
        description='Console client for synchronizing and retrieving data about currencies'
    )
    subparsers = parser.add_subparsers(
        title='commands',
        description='CLI commands',
        dest='command'
    )

    # Fill command
    fill_parser = subparsers.add_parser(
        'fill',
        help='Fills the database with exchange rate data for a certain period'
    )
    fill_parser.add_argument(
        '--year', '-y',
        type=str,
        help='The year you want to fill in the information about',
        required=True
    )

    # Schedule command
    schedule_parser = subparsers.add_parser(
        'schedule',
        help='Start a scheduled task, which will save the current course in the database.'
    )
    schedule_parser.add_argument(
        '--interval', '-i',
        help='Interval between filling database (in days)',
        required=True,
        type=int
    )

    # Start server command
    server_parser = subparsers.add_parser(
        'launch',
        help='Start a web API, which provides reports on different currencies over a period of time'
    )
    server_parser.add_argument(
        '--config', '-c',
        help='Path to server\'s config file',
        required=True
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == 'fill':
        fill_db(args.year)
    elif args.command == 'schedule':
        schedule_task(args.interval)
    elif args.command == 'launch':
        start_server(args.config)
    else:
        raise NotImplementedError('No such commands')


if __name__ == '__main__':
    main()
