"""
    Author
    sergioRG
"""
import argparse
import logging
import uuid

EXTRA_ATTRS = ['hub_honesty_factor']

def parse_options():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-file',
        help='Input file with a history report from history.py'
    )


    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug messages'
        )

    return parser.parse_args()


def main(input_file, debug):

    output_base = f'{input_file}-{uuid.uuid4()}'

    if debug:
        logging.basicConfig(filename=f'{output_base}.log', level=logging.DEBUG)

    with open(input_file, 'r') as f:
        report_d = eval(f.read())

    for (hub_name, matches) in [(k, v) for (k, v) in report_d.items() if k not in EXTRA_ATTRS]:
        win_rate = 100.0 * sum([match['player_won'] / len(matches) for match in matches])
        average_dishonesty = sum([1.0 * match['dishonesty_factor'] / len(matches) for match in matches])
        print(f'{hub_name}: {len(matches)} matches, {win_rate:.2f}% WR, {average_dishonesty:.2f} DF')
        print()

if __name__ == '__main__':
    opts = parse_options()
    main(**vars(opts))
