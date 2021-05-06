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

try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

from validations_common.library import warn


class TestWarn(base.TestCase):
    def setUp(self):
        super(TestWarn, self).setUp()
        self.warn = warn
        self.module = mock.MagicMock()
        self.module.params = {'msg': 'foo'}

    @mock.patch(
        'validations_common.library.warn.AnsibleModule')
    @mock.patch(
        'validations_common.library.warn.yaml_safe_load',
        return_value={'options': mock.MagicMock()})
    def test_warn_run(self, mock_safe_load, mock_ansible_module):
        """Verify that warn correctly works with provided YAML.
        """
        mock_module = mock.MagicMock()
        mock_module.params = {'msg': 'foo'}
        mock_ansible_module.return_value = mock_module

        self.warn.main()

        mock_safe_load.assert_called_once_with(self.warn.DOCUMENTATION)
        mock_module.exit_json.assert_called_once_with(
            changed=False,
            warnings=['foo'])

    def test_warn_attributes(self):
        """Verify that module contains required attributes.
        """

        required_names = set(
            [
                'DOCUMENTATION',
                'EXAMPLES',
                'AnsibleModule'
            ])

        warn_names = set(dir(self.warn))
        self.assertTrue(warn_names.issuperset(required_names))
