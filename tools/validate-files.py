#!/usr/bin/env python
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import os
import sys


def exit_usage():
    print('Usage {} <directory>'.format(sys.argv[0]))
    sys.exit(1)


def validate_library_file(file_path, quiet):

    with open(file_path) as f:
        file_content = f.read()
        if 'DOCUMENTATION = ' not in file_content \
                or 'EXAMPLES = ' not in file_content:
            if quiet < 3:
                print('Missing ansible documentation in {}'.format(file_path))
            return 1
    return 0


def validate_callback_file(file_path, quiet):
    required_attributes = [
        'CALLBACK_VERSION',
        'CALLBACK_NAME']

    with open(file_path) as file:
        file_content = file.read()
        if any([attr not in file_content for attr in required_attributes]):
            if quiet < 3:
                print(
                    'Missing required callback plugin attributes in {}'.format(file_path))
            return 1
    return 0


def validate_file(file_path, quiet):
    if os.path.split(file_path)[0].endswith('library'):
        return validate_library_file(file_path, quiet)
    elif os.path.split(file_path)[0].endswith('callback_plugins'):
        return validate_callback_file(file_path, quiet)
    else:
        raise ValueError()


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--quiet', '-q',
                   action='count',
                   default=0,
                   help='output warnings and errors (-q) or only errors (-qq)')

    p.add_argument('path_args',
                   nargs='*',
                   default=['.'])

    return p.parse_args()


def main():
    args = parse_args()
    path_args = args.path_args
    quiet = args.quiet
    exit_val = 0
    scanned_subdirs = ['callback_plugins', 'library']
    failed_files = []

    for base_path in path_args:
        scanned_paths = [
            os.path.join(
                base_path,
                'validations_common',
                path) for path in scanned_subdirs]

        if os.path.isdir(base_path):
            for subdir, dirs, files in os.walk(base_path):
                if '.tox' in dirs:
                    dirs.remove('.tox')
                if '.git' in dirs:
                    dirs.remove('.git')
                if subdir in scanned_paths:
                    for f in files:
                        if f.endswith('.py') and f != '__init__.py':
                            file_path = os.path.join(subdir, f)
                            if quiet < 1:
                                print('Validating {}'.format(file_path))
                            failed = validate_file(file_path, quiet)
                            if failed:
                                failed_files.append(file_path)
                            exit_val |= failed
        else:
            print('Unexpected argument {}'.format(base_path))
            exit_usage()

    if failed_files:
        print('Validation failed on:')
        for f in failed_files:
            print(f)
    else:
        print('Validation successful!')
    sys.exit(exit_val)

if __name__ == '__main__':
    main()
