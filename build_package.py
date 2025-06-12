"""

"""

#!/usr/bin/env python3
import sys

from time import time

import os
import logging
import re
import subprocess
from argparse import ArgumentParser
from configparser import ConfigParser

logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.INFO)

script_name = os.path.basename(__file__)
log = logging.getLogger(script_name)

parser = ArgumentParser(script_name)
parser.add_argument('--dry-run', action='store_true', required=False)
parser.add_argument('--pre-release', required=False)  # a=alpha, b=beta, rc=release-candidate
parser.add_argument('--add-random-bit', action='store_true', required=False)
parser.add_argument('--ignore-unsaved', action='store_true', required=False)
parser.add_argument('--version', required=False)
args = parser.parse_args()


def install_build_tool_dependency(*package_names):
    subprocess.call(['python3', '-m', 'pip', 'install', '-q', *package_names])


def main():
    in_dry_run_mode = args.dry_run

    # Set up the build environment.
    if in_dry_run_mode:
        log.warning('The build environment is not maintained because the script is in the dry run mode.')
    else:
        log.info('Ensuring the minimum build requirements...')
        install_build_tool_dependency(
            'build>=0.7.0',
            'setuptools>=49.2.1'
        )

    # Determine the release version
    if args.version:
        release_version = args.version
    else:
        changes = [
            (change_type, file_path)
            for change_type, file_path in [
                re.split(r' +', l.strip())
                for l in subprocess.check_output(['git', 'status', '--short', '-uno'],
                                                 universal_newlines=True).split('\n')
                if l
            ]
            if not file_path.startswith('scripts') and file_path not in ('cloudbuild.yaml', 'Makefile')
        ]
        if changes and not args.ignore_unsaved:
            log.warning('Changes detected:')
            for change_type, file_path in changes:
                log.warning(f' - [{change_type}] {file_path}')
            log.error('Please commit the changes or stash them before running this script.')
            sys.exit(1)

        log.info('Determining the release version...')
        git_version = subprocess.check_output(['git', 'describe'], universal_newlines=True).strip()
        log.info(f'Version/GIT: {git_version}')

        try:
            base_version, revision_number, __ = git_version.split(r'-')
        except ValueError:
            base_version = git_version
            revision_number = '0'
        split_base_version = base_version.split(r'.')
        major_version = split_base_version[0]
        minor_version = split_base_version[1]

        release_version = f'{major_version}.{minor_version}.{revision_number}'

    if args.pre_release:
        release_version = release_version + args.pre_release
        if args.add_random_bit:
            release_version = release_version + str(int(time()))

    log.info(f'Version/Release: {release_version}')

    # Update dnastack.constants
    with open('dnastack/constants.py', 'r') as f:
        content = f.read()
    content = re.sub(r'__version__\s*=\s*[^\s]+', f'__version__ = "{release_version}"', content)
    if in_dry_run_mode:
        log.info(f'dnastack.constants:\n\n{content}')
    else:
        with open('dnastack/constants.py', 'w') as f:
            f.write(content)

    # Update setup.cfg
    setup_file_path = 'setup.cfg'
    setup_config = ConfigParser()
    setup_config.read(setup_file_path)
    setup_config['metadata']['version'] = release_version
    if in_dry_run_mode:
        setup_temp_file = 'setup_dryrun.cfg'
        with open(setup_temp_file, 'w') as f:
            setup_config.write(f)
        with open(setup_temp_file, 'r') as f:
            log.info(f'setup.cfg:\n\n{f.read()}')
        os.unlink(setup_temp_file)
    else:
        with open(setup_file_path, 'w') as f:
            setup_config.write(f)

    # Build the package
    if args.dry_run:
        log.warning('The package will not be built because the script is in the dry run mode.')
    else:
        log.info('Building the package...')
        subprocess.call(['python3', '-m', 'build'])

    log.info('Cleaning up...')

    subprocess.call(['git', 'checkout', '--', 'setup.cfg', 'dnastack/constants.py'])

    log.info('Done')


if __name__ == '__main__':
    main()