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

from unittest import mock
from validations_common.library import advanced_format
from validations_common.tests import base


class TestAdvancedFormat(base.TestCase):
    def setUp(self):
        super(TestAdvancedFormat, self).setUp()
        self.read_int = advanced_format.read_int

    @mock.patch('ansible.module_utils.basic.AnsibleModule', autospec=True)
    @mock.patch('six.moves.builtins.open', autospec=True)
    def test_read_int(self, mock_open, mock_module):

        args = {
            'module': mock_module,
            'file_path': './foo/bar'
        }
        self.read_int(**args)

        mock_open.assert_called_once_with(args['file_path'])
