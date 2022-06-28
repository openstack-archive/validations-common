# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Ansible module to read a value from an INI file.
Usage:
validations_read_ini: path=/path/to/file.ini section=default key=something

This will read the `path/to/file.ini` file and read the `Hello!` value under:
    [default]
    something = Hello!

You can register the result and use it later with `{{ my_ini.value }}`
"""

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser

from enum import Enum
import os

from ansible.module_utils.basic import AnsibleModule
from yaml import safe_load as yaml_safe_load


DOCUMENTATION = '''
---
module: validations_read_ini
short_description: Get data from an ini file
description:
    - Get data from an ini file
options:
    path:
        required: true
        description:
            - File path
        type: str
    section:
        required: true
        description:
            - Section to look up
        type: str
    key:
        required: true
        description:
            - Section key to look up
        type: str
    default:
        required: false
        description:
            - Default value if key isn't found
    ignore_missing_file:
        required: false
        description:
            - Flag if a missing file should be ignored
        type: bool
author: "Tomas Sedovic"
'''

EXAMPLES = '''
- hosts: fizzbuz
  tasks:
    - name: Lookup bar value
      validations_read_ini:
        path: config.ini
        section: foo
        key: bar
        ignore_missing_file: True
      register: bar_value
'''


# Possible return values
class ReturnValue(Enum):
    OK = 0
    INVALID_FORMAT = 1
    KEY_NOT_FOUND = 2


def check_file(path):
    """Check if the requested file exists.
    :param path: path to configuration file
    :dtype path: `string`

    :returns: True if file exists, false otherwise
    :rtype: `bool`
    """

    return (os.path.exists(path) and os.path.isfile(path))


def get_result(path, section, key, default=None):
    """Get value based on a section and a key.

    :param path: path to configuration file
    :dtype path: `string`
    :param section: name of the config file section
    :dtype section: `string`
    :param key: key for which we want to know the value
    :dtype key: `string`
    :param default: default value to use if the key does not exist
    :dtype default: `object`

    :returns: tuple of numeric return code, message and value of the requested key
    :rtype: `tuple`
    """

    msg = ''
    value = None
    config = ConfigParser.SafeConfigParser(strict=False)

    try:
        config.read(path)
    except (OSError, ConfigParser.ParsingError) as exc_msg:
        msg = "The file '{}' is not in a valid INI format: {}".format(
            path, exc_msg)
        return (ReturnValue.INVALID_FORMAT, msg, value)

    try:
        value = config.get(section, key)
        msg = ("The key '{}' under the section '{}' in file {} "
               "has the value: '{}'").format(key, section, path, value)
        ret = ReturnValue.OK
    except ConfigParser.Error:
        if default:
            msg = ("There is no key '{}' under section '{}' in file {}. Using"
                   " default value '{}'".format(key, section, path, default))
            ret = ReturnValue.OK
            value = default
        else:
            value = None
            msg = "There is no key '{}' under the section '{}' in file {}.".format(
                  key, section, path)
            ret = ReturnValue.KEY_NOT_FOUND
    return (ret, msg, value)


def main():
    module = AnsibleModule(
        argument_spec=yaml_safe_load(DOCUMENTATION)['options'])

    ini_file_path = module.params.get('path')
    ignore_missing = module.params.get('ignore_missing_file')

    # Check that file exists
    file_exists = check_file(ini_file_path)

    if file_exists:
        # Try to parse the result from ini file
        section = module.params.get('section')
        key = module.params.get('key')
        default = module.params.get('default')

        ret, msg, value = get_result(ini_file_path, section, key, default)

        if ret == ReturnValue.INVALID_FORMAT:
            module.fail_json(msg=msg)
        elif ret == ReturnValue.KEY_NOT_FOUND:
            module.exit_json(msg=msg, changed=False, value=None)
        elif ret == ReturnValue.OK:
            module.exit_json(msg=msg, changed=False, value=value)
    else:
        # Opening file failed
        msg = "Could not open the ini file: '{}'".format(ini_file_path)
        if ignore_missing:
            module.exit_json(msg=msg, changed=False, value=None)
        else:
            module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
