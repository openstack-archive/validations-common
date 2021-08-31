# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_validations_read_ini
----------------------------------

Tests for `validations_read_ini` module.
"""


import os
import tempfile

try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

import validations_common.library.validations_read_ini as validation

invalid_content = '''
[DEFAULT#
    hello =
'''

valid_content = '''
[DEFAULT]
debug=True

[dhcp]
dhcp_start=192.168.0.1
dhcp_end=192.168.0.254

[secrets]
password=1234
'''


class TestValidationsReadIni(base.TestCase):

    def test_check_file_invalid_path(self):
        '''Test validations_read_ini when path is invalid'''

        ret_val = validation.check_file('non/existing/path')
        self.assertEqual(False, ret_val)

    def test_check_file_valid_path(self):
        '''Test validations_read_ini when path is valid'''

        with self.create_tmp_ini() as tmpfile:
            tmp_name = os.path.relpath(tmpfile.name)
            ret_val = validation.check_file(tmp_name)
        tmpfile.close()

        self.assertEqual(True, ret_val)

    def test_get_result_invalid_format(self):
        '''Test validations_read_ini when file format is valid'''

        tmpfile = self.create_tmp_ini()
        tmp_name = os.path.relpath(tmpfile.name)
        tmpfile.write(invalid_content.encode('utf-8'))
        tmpfile.seek(0)
        ret, msg, value = validation.get_result(tmp_name, 'section', 'key')
        tmpfile.close()

        self.assertEqual(validation.ReturnValue.INVALID_FORMAT, ret)
        asserted = ("The file '{path}' is not in a valid INI format: File "
                    "contains no section headers.\nfile: '{path}', line: 2\n"
                    "'[DEFAULT#\\n\'").format(path=tmp_name)

        self.assertEqual(asserted, msg)
        self.assertIsNone(value)

    def test_get_result_key_not_found(self):
        '''Test validations_read_ini when key is not found'''

        tmpfile = self.create_tmp_ini()
        tmp_name = os.path.relpath(tmpfile.name)
        tmpfile.write(valid_content.encode('utf-8'))
        tmpfile.seek(0)
        ret, msg, value = validation.get_result(tmp_name, 'section', 'key')
        tmpfile.close()

        self.assertEqual(validation.ReturnValue.KEY_NOT_FOUND, ret)
        self.assertEqual(("There is no key 'key' under the section 'section' "
                          "in file {}.").format(tmp_name), msg)
        self.assertIsNone(value)

    def test_get_result_key_not_found_with_default(self):
        '''Test validations_read_ini when key is not found but has a default'''

        tmpfile = self.create_tmp_ini()
        tmp_name = os.path.relpath(tmpfile.name)
        tmpfile.write(valid_content.encode('utf-8'))
        tmpfile.seek(0)
        ret, msg, value = validation.get_result(tmp_name, 'section', 'key',
                                                'foo')
        tmpfile.close()

        self.assertEqual(validation.ReturnValue.OK, ret)
        self.assertEqual(("There is no key 'key' under section 'section' "
                          "in file {}. Using default value '{}'"
                          ).format(tmp_name, 'foo'), msg)
        self.assertEqual(value, 'foo')

    def test_get_result_ok(self):
        '''Test validations_read_ini when key is not found'''

        tmpfile = self.create_tmp_ini()
        tmp_name = os.path.relpath(tmpfile.name)
        tmpfile.write(valid_content.encode('utf-8'))
        tmpfile.seek(0)
        ret, msg, value = validation.get_result(tmp_name, 'secrets',
                                                'password')
        tmpfile.close()

        self.assertEqual(validation.ReturnValue.OK, ret)
        self.assertEqual(("The key 'password' under the section 'secrets'"
                          " in file {} has the value: '1234'").format(
                         tmp_name), msg)
        self.assertEqual('1234', value)

    def create_tmp_ini(self):
        '''Create temporary tmp.ini file, return its full name'''

        path = 'validations_common/tests'
        tmpfile = tempfile.NamedTemporaryFile(suffix='.ini', prefix='tmp',
                                              dir=path)
        return tmpfile
