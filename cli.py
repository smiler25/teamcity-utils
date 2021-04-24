import argparse

from methods import TeamCity


def create_parser():
    p = argparse.ArgumentParser()
    p.add_argument('-b', '--branch', default='refs/heads/master', help='Build branch')
    p.add_argument('-s', '--services', nargs='+', help='Services to build')
    p.add_argument('-l', '--list', action='store_true', default=False, help='Show services')
    p.add_argument('-p', '--personal', action='store_true', default=False, help='Personal build')
    return p


if __name__ == '__main__':
    tc = TeamCity()
    parser = create_parser()
    args = parser.parse_args()
    if not args.list and not args.services:
        print('Specify arguments')
        exit()

    if args.list:
        ok, grouped_services = tc.get_services()
        if ok:
            print('Title -> Key')
            for project_name, services in grouped_services.items():
                print('\nProject: {}'.format(project_name))
                for k, v in services:
                    print(v, k, sep=' -> ')
        else:
            print('Error', grouped_services)
        exit()

    branch = args.branch
    if not branch:
        raise Warning('Specify branch')

    for service in args.services:
        ok, msg = tc.run_build(service, branch, args.personal)
        if ok:
            print(service, 'Done!')
        else:
            print(service, 'Fail', msg)
