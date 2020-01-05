import argparse
from .methods import TeamCity


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--branch', default='refs/heads/master', help='Build branch')
    parser.add_argument('-s', '--services', nargs='+', help='Services to build')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='Show services')
    return parser


if __name__ == '__main__':
    tc = TeamCity()
    parser = create_parser()
    args = parser.parse_args()
    if args.list:
        print(tc.get_services()[1])
        exit()

    branch = args.branch
    if not branch:
        raise Warning('Specify branch')
    for service in args.services:
        if tc.run_build(service, branch):
            print('Done!')
        else:
            print('Fail')
