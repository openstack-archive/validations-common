# Copyright 2017 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Check for available updates for a given package.
Module queries and parses output of at least two separate
external binaries, in order to obtain information about
supported package manager, installed and available packages.
As such it has many points of failure.

Information about supported package managers,
such as the commands to use while working with them
and the expected stderr output we can encounter while querying repos,
are stored as a nested dictionery SUPPORTED_PKG_MGRS.
With names of the supported package managers as keys
of the first level elements. And the aformentioned information
on the second level, as lists of strings, with self-explanatory keys.

Formally speaking it is a tree of a sort.
But so is entire python namespace.
"""

import collections
import subprocess

from ansible.module_utils.basic import AnsibleModule
from yaml import safe_load as yaml_safe_load

DOCUMENTATION = '''
---
module: check_package_update
short_description: Check for available updates for given packages
description:
    - Check for available updates for given packages
options:
    packages_list:
        required: true
        description:
            - The names of the packages you want to check
        type: list
    pkg_mgr:
        required: false
        description:
            - Supported Package Manager, DNF or YUM
        type: str
author:
    - Florian Fuchs
    - Jiri Podivin (@jpodivin)
'''

EXAMPLES = '''
- hosts: webservers
  tasks:
    - name: Get available updates for packages
      check_package_update:
        packages_list:
          - coreutils
          - wget
        pkg_mgr: "{{ ansible_pkg_mgr }}"
'''

SUPPORTED_PKG_MGRS = {
    'dnf': {
        'query_installed': [
            'rpm', '-qa', '--qf',
            '%{NAME}|%{VERSION}|%{RELEASE}|%{ARCH}\n'
        ],
        'query_available': [
            'dnf', '-q', 'list', '--available'
        ],
        'allowed_errors': [
            '',
            'Error: No matching Packages to list\n'
        ]
    },
    'yum': {
        'query_installed': [
            'rpm', '-qa', '--qf',
            '%{NAME}|%{VERSION}|%{RELEASE}|%{ARCH}\n'
        ],
        'query_available': [
            'yum', '-q', 'list', 'available'
        ],
        'allowed_errors': [
            '',
            'Error: No matching Packages to list\n'
        ]
    },
}


PackageDetails = collections.namedtuple(
    'PackageDetails',
    ['name', 'version', 'release', 'arch'])


def get_package_details(pkg_details_string):
    """Returns PackageDetails namedtuple from given string.
    Raises ValueError if the number of '|' separated
    fields is < 4.

    :return: package details
    :rtype: collections.namedtuple
    """
    split_output = pkg_details_string.split('|')
    try:
        pkg_details = PackageDetails(
            split_output[0],
            split_output[1],
            split_output[2],
            split_output[3],
        )
    except IndexError:
        raise ValueError(
            (
                "Package description '{}' doesn't contain fields"
                " required for processing."
            ).format(pkg_details_string)
        )

    return pkg_details


def _allowed_pkg_manager_stderr(stderr, allowed_errors):
    """Returns False if the error message isn't in the
    allowed_errors list.
    This function factors out large, and possibly expanding,
    condition so it doesn't cause too much confusion.
    """

    if stderr in allowed_errors:
        return True
    return False


def _command(command):
    """
    Return result of a subprocess call.
    Doesn't set timeout for the call, so the process can hang.
    Potentially for a very long time.
    :return: stdout and stderr from Popen.communicate()
    :rtype: tuple
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

    return process.communicate()


def _get_pkg_manager(module):
    """Return name of available package manager.
    Queries binaries using `command -v`, in order defined by
    the `SUPPORTED_PKG_MGRS`.
    :returns: string
    """
    for possible_pkg_mgr in SUPPORTED_PKG_MGRS:

        stdout, stderr = _command(['command', '-v', possible_pkg_mgr])
        if stdout != '' and stderr == '':
            return possible_pkg_mgr

    module.fail_json(
        msg=(
            "None of the supported package managers '{}' seems to be "
            "available on this system."
        ).format(' '.join(SUPPORTED_PKG_MGRS))
    )


def _get_new_pkg_info(available_stdout):
    """Return package information as dictionary. With package names
    as keys and detailed information as list of strings.
    """
    available_stdout = available_stdout.split('\n')[1:]

    available_stdout = [line.rstrip().split() for line in available_stdout]

    new_pkgs_info = {}

    for line in available_stdout:
        if len(line) != 0:
            new_pkgs_info[line[0]] = PackageDetails(
                line[0],
                line[1].split('-')[0],
                line[1].split('-')[1],
                line[0].split('.')[1])

    return new_pkgs_info


def _get_installed_pkgs(installed_stdout, packages, module):
    """Return dictionary of installed packages.
    Package names form keys and the output of the get_package_details
    function values of the dictionary.
    """
    installed = {}
    installed_stdout = installed_stdout.split('\n')[:-1]

    for package in installed_stdout:
        if package != '':
            package = get_package_details(package)
            if package.name in packages:
                installed[package.name + '.' + package.arch] = package
                packages.remove(package.name)
        #Once find all the requested packages we don't need to continue search
        if len(packages) == 0:
            break

    #Even a single missing package is a reason for failure.
    if len(packages) > 0:
        msg = "Following packages are not installed {}".format(packages)
        module.fail_json(
            msg=msg
        )
        return

    return installed


def check_update(module, packages_list, pkg_mgr):
    """Check if the packages in the 'packages_list are up to date.
    Queries binaries, defined the in relevant SUPPORTED_PKG_MGRS entry,
    to obtain information about present and available packages.

    :param module: ansible module providing fail_json and exit_json
                   methods
    :type module: AnsibleModule
    :param packages_list: list of packages to be checked
    :type package: list
    :param pkg_mgr: Package manager to check for update availability
    :type pkg_mgr: string

    :return: None
    :rtype: None
    """
    if len(packages_list) == 0:
        module.fail_json(
            msg="No packages given to check.")
        return

    if pkg_mgr is None:
        pkg_mgr = _get_pkg_manager(module=module)
    if pkg_mgr not in SUPPORTED_PKG_MGRS:
        module.fail_json(
            msg='Package manager "{}" is not supported.'.format(pkg_mgr))
        return

    pkg_mgr = SUPPORTED_PKG_MGRS[pkg_mgr]

    installed_stdout, installed_stderr = _command(pkg_mgr['query_installed'])

    # Fail the module if for some reason we can't lookup the current package.
    if installed_stderr != '':
        module.fail_json(msg=installed_stderr)
        return
    if not installed_stdout:
        module.fail_json(
            msg='no output returned for the query.{}'.format(
                ' '.join(pkg_mgr['query_installed'])
            ))
        return

    installed = _get_installed_pkgs(installed_stdout, packages_list, module)

    installed_pkg_names = ' '.join(installed)

    pkg_mgr['query_available'].append(installed_pkg_names)

    available_stdout, available_stderr = _command(pkg_mgr['query_available'])

    #We need to check that the stderr consists only of the expected strings
    #This can get complicated if the CLI on the pkg manager side changes.
    if not _allowed_pkg_manager_stderr(available_stderr, pkg_mgr['allowed_errors']):
        module.fail_json(msg=available_stderr)
        return
    if available_stdout:
        new_pkgs_info = _get_new_pkg_info(available_stdout)
    else:
        new_pkgs_info = {}

    results = []

    for installed_pkg in installed:

        results.append(
            {
                'name': installed_pkg,
                'current_version': installed[installed_pkg].version,
                'current_release': installed[installed_pkg].release,
                'new_version': None,
                'new_release': None
            }
        )

        if installed_pkg in new_pkgs_info:
            results[-1]['new_version'] = new_pkgs_info[installed_pkg][1]
            results[-1]['new_release'] = new_pkgs_info[installed_pkg][2]

    module.exit_json(
        changed=False,
        outdated_pkgs=results
    )


def main():
    module = AnsibleModule(
        argument_spec=yaml_safe_load(DOCUMENTATION)['options']
    )

    check_update(
        module,
        packages_list=module.params.get('packages_list'),
        pkg_mgr=module.params.get('pkg_mgr', None))


if __name__ == '__main__':
    main()
