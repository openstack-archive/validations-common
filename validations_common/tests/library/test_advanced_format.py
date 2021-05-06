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

from validations_common.library import advanced_format


class TestAdvancedFormat(base.TestCase):
    def setUp(self):
        super(TestAdvancedFormat, self).setUp()
        self.read_int = advanced_format.read_int
        self.advanced_format = advanced_format
        self.module = mock.MagicMock()
        self.module.params = {'msg': 'foo'}

    @mock.patch(
        'validations_common.library.advanced_format.read_int',
        return_value=0)
    @mock.patch(
        'validations_common.library.advanced_format.AnsibleModule')
    @mock.patch(
        'validations_common.library.advanced_format.yaml_safe_load',
        return_value={'options': mock.MagicMock()})
    def test_advanced_format_run_same_sizes(self, mock_safe_load,
                                            mock_ansible_module,
                                            mock_read_int):
        """Verify that advanced_format correctly works with provided YAML.
        """

        mock_module = mock.MagicMock()
        mock_module.params = {'drive': 'foo'}
        mock_ansible_module.return_value = mock_module

        self.advanced_format.main()
        mock_safe_load.assert_called_once_with(self.advanced_format.DOCUMENTATION)

        mock_module.exit_json.assert_called_once_with(
            changed=False,
            msg="The disk foo probably doesn't use Advance Format.")

    @mock.patch(
        'validations_common.library.advanced_format.read_int',
        side_effect=[100, 1000])
    @mock.patch(
        'validations_common.library.advanced_format.AnsibleModule')
    @mock.patch(
        'validations_common.library.advanced_format.yaml_safe_load',
        return_value={'options': mock.MagicMock()})
    def test_advanced_format_run_different_sizes(self, mock_safe_load,
                                                 mock_ansible_module,
                                                 mock_read_int):
        """Verify that advanced_format correctly works with provided YAML.
        """

        mock_module = mock.MagicMock()
        mock_module.params = {'drive': 'foo'}
        mock_ansible_module.return_value = mock_module

        self.advanced_format.main()
        mock_safe_load.assert_called_once_with(self.advanced_format.DOCUMENTATION)

        mock_module.exit_json.assert_called_once_with(
            changed=True,
            warnings=mock.ANY)

    def test_advanced_format_attributes(self):
        """Verify that module contains required attributes.
        """
        required_names = set(
            [
                'DOCUMENTATION',
                'EXAMPLES',
                'AnsibleModule'
            ])
        advanced_format_names = set(dir(self.advanced_format))
        self.assertTrue(advanced_format_names.issuperset(required_names))

    @mock.patch('ansible.module_utils.basic.AnsibleModule', autospec=True)
    @mock.patch('six.moves.builtins.open', autospec=True)
    def test_read_int(self, mock_open, mock_module):

        args = {
            'module': mock_module,
            'file_path': './foo/bar'
        }
        self.read_int(**args)

        mock_open.assert_called_once_with(args['file_path'])

    @mock.patch('ansible.module_utils.basic.AnsibleModule', autospec=True)
    @mock.patch(
        'six.moves.builtins.open',
        autospec=True,
        side_effect=IOError())
    def test_read_int_ioerror(self, mock_open, mock_module):
        """Verify that IOError causes fail_json call.

        As the msg argument is ultimately a string and subject
        to potential changes without effect on its function, we only verify
        the presence of call.
        """
        args = {
            'module': mock_module,
            'file_path': './foo/bar'
        }

        self.read_int(**args)

        mock_open.assert_called_once_with(args['file_path'])
        mock_module.fail_json.assert_called_once()

    @mock.patch(
        'validations_common.library.advanced_format.int',
        side_effect=ValueError())
    @mock.patch('ansible.module_utils.basic.AnsibleModule', autospec=True)
    @mock.patch('six.moves.builtins.open', autospec=True)
    def test_read_int_valueerror(self, mock_open, mock_module, mock_adv_format_int):
        """Verify that ValueError raised by int conversion
        causes fail_json call.

        As the msg argument is ultimately a string and subject
        to potential changes without effect on its function, we only verify
        the presence of call.
        """
        args = {
            'module': mock_module,
            'file_path': './foo/bar'
        }

        self.read_int(**args)

        mock_open.assert_called_once_with(args['file_path'])
        mock_module.fail_json.assert_called_once()
