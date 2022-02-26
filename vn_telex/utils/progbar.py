import sys


def print_bar(width=30, empty='-', fill='■', percentage=0, message=''):
    fill_count = round(percentage / 100 * width)
    bar = fill * fill_count + empty * (width - fill_count)
    sys.stdout.write(
        f'\r[{bar}] '
        f'{percentage}% '
        f'{message}'
    )
    sys.stdout.flush()


def print_done(message='[DONE]', end='\n'):
    sys.stdout.write(f'\r{message}{end}')
    sys.stdout.flush()
