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

from validations_common.library import check_package_update as cppkg

PKG_INSTALLED = "foo-package|6.1.5|1|x86_64"
PKG_INVALID = "foo-package|6.1.5|x86_64"
PKG_AVAILABLE = """\
Available Packages
foo-package.x86_64        8.0.0-1         foo-stable
"""


class TestGetPackageDetails(base.TestCase):
    def setUp(self):
        super(TestGetPackageDetails, self).setUp()
        self.entry = PKG_INSTALLED
        self.invalid_pkg = PKG_INVALID

    def test_name(self):
        details = cppkg.get_package_details(self.entry)
        self.assertEqual(details.name, 'foo-package')

    def test_arch(self):
        details = cppkg.get_package_details(self.entry)
        self.assertEqual(details.arch, 'x86_64')

    def test_version(self):
        details = cppkg.get_package_details(self.entry)
        self.assertEqual(details.version, '6.1.5')

    def test_release(self):
        details = cppkg.get_package_details(self.entry)
        self.assertEqual(details.release, '1')

    def test_index_error(self):
        self.assertRaises(ValueError, cppkg.get_package_details, self.invalid_pkg)


class TestCheckUpdate(base.TestCase):
    def setUp(self):
        super(TestCheckUpdate, self).setUp()
        self.module = mock.MagicMock()
        self.package_details = cppkg.get_package_details("foo-package|6.1.5|1|x86_64")

    def test_empty_pkg_list_fails(self):

        cppkg.check_update(self.module, [], 'dnf')

        self.module.fail_json.assert_called_once_with(
            msg='No packages given to check.')

        self.module.reset_mock()

    def test_unsupported_pkg_mgr_fails(self):

        cppkg.check_update(self.module, ['foo-package'], 'apt')

        self.module.fail_json.assert_called_with(
            msg='Package manager "apt" is not supported.')

        self.module.reset_mock()

    @mock.patch('validations_common.library.check_package_update._command')
    def test_fails_if_installed_package_not_found(self, mock_command):
        mock_command.side_effect = [
            ['', 'No package found.'],
        ]

        cppkg.check_update(self.module, ['foo-package'], 'yum')

        self.module.fail_json.assert_called_with(
            msg='No package found.')

        self.module.reset_mock()

    @mock.patch(
        'validations_common.library.check_package_update._get_new_pkg_info',
        return_value={
            'foo-package.x86_64': cppkg.PackageDetails(
                'foo-package.x86_64',
                '8.0.0',
                '1',
                'foo-stable')
        }
    )
    @mock.patch(
        'validations_common.library.check_package_update._get_installed_pkgs')
    @mock.patch('validations_common.library.check_package_update._command')
    def test_returns_current_and_available_versions(self, mock_command,
                                                    mock_get_installed, mock_get_new_pkg_info):

        mock_command.side_effect = [
            [PKG_INSTALLED, ''],
            [PKG_AVAILABLE, ''],
        ]

        mock_get_installed.side_effect = [{'foo-package.x86_64': self.package_details}]

        cppkg.check_update(self.module, ['foo-package'], 'yum')

        mock_get_installed.assert_called_once_with(
            PKG_INSTALLED,
            ['foo-package'],
            self.module)

        self.module.exit_json.assert_called_with(
            changed=False,
            outdated_pkgs=[
                {
                    'name': 'foo-package.x86_64',
                    'current_version': '6.1.5',
                    'current_release': '1',
                    'new_version': '8.0.0',
                    'new_release': '1'
                }
            ])

        self.module.reset_mock()

    @mock.patch(
        'validations_common.library.check_package_update._get_new_pkg_info',
        return_value={
            'foo-package.x86_64': cppkg.PackageDetails(
                'foo-package.x86_64',
                '8.0.0',
                '1',
                'foo-stable')
        }
    )
    @mock.patch(
        'validations_common.library.check_package_update._get_installed_pkgs')
    @mock.patch('validations_common.library.check_package_update._command')
    def test_returns_current_version_if_no_updates(self, mock_command,
                                                   mock_get_installed, mock_get_new_pkg_info):
        mock_command.side_effect = [
            [PKG_INSTALLED, ''],
            ['', 'Error: No matching Packages to list\n'],
        ]

        mock_get_installed.side_effect = [{'foo-package.x86_64': self.package_details}]

        cppkg.check_update(self.module, ['foo-package'], 'yum')

        mock_get_installed.assert_called_once_with(
            PKG_INSTALLED,
            ['foo-package'],
            self.module)

        self.module.exit_json.assert_called_with(
            changed=False,
            outdated_pkgs=[
                {
                    'name': 'foo-package.x86_64',
                    'current_version': '6.1.5',
                    'current_release': '1',
                    'new_version': None,
                    'new_release': None
                }
            ])

        self.module.reset_mock()

    @mock.patch(
        'validations_common.library.check_package_update.subprocess.PIPE')
    @mock.patch(
        'validations_common.library.check_package_update.subprocess.Popen')
    def test_command_rpm_no_process(self, mock_popen, mock_pipe):

        cli_command = [
            'rpm',
            '-qa',
            '--qf',
            '%{NAME}|%{VERSION}|%{RELEASE}|%{ARCH}\n'
        ]

        command_output = cppkg._command(cli_command)

        mock_popen.assert_called_once_with(
            cli_command,
            stdout=mock_pipe,
            stderr=mock_pipe,
            universal_newlines=True)

    def test_get_new_pkg_info(self):

        pkg_info = cppkg._get_new_pkg_info(PKG_AVAILABLE)

        self.assertIsInstance(pkg_info, dict)
        self.assertTrue('foo-package.x86_64' in pkg_info)
        self.assertIsInstance(pkg_info['foo-package.x86_64'], cppkg.PackageDetails)

    @mock.patch('validations_common.library.check_package_update._command')
    def test_get_pkg_mgr_fail(self, mock_command):

        mock_command.side_effect = [
            ('barSTDOUT', 'fooERROR'),
            ('', '')
        ]

        pkg_manager = cppkg._get_pkg_manager(self.module)

        self.assertEqual(pkg_manager, None)
        self.module.fail_json.assert_called_once_with(msg=mock.ANY)

        self.module.reset_mock()

    @mock.patch('validations_common.library.check_package_update._command')
    def test_get_pkg_mgr_succes_dnf(self, mock_command):
        mock_command.side_effect = [('fizzSTDOUT', '')]

        pkg_manager = cppkg._get_pkg_manager(self.module)

        self.assertEqual(pkg_manager, 'dnf')
        self.module.fail_json.assert_not_called()

        self.module.reset_mock()

    @mock.patch('validations_common.library.check_package_update._command')
    def test_get_pkg_mgr_succes_yum(self, mock_command):
        mock_command.side_effect = [
            ('barSTDOUT', 'fooERROR'),
            ('fizzSTDOUT', '')
        ]

        pkg_manager = cppkg._get_pkg_manager(self.module)

        self.assertEqual(pkg_manager, 'yum')
        self.module.fail_json.assert_not_called()

        self.module.reset_mock()

    def test_get_installed_pkgs_success(self):
        """Test that _get_installed_pkgs will correctly process
        output of rpm, compare it with provided package name list
        and return dictionary of PackageDetails.
        """

        installed_pkgs = cppkg._get_installed_pkgs(
            PKG_INSTALLED + '\n',
            ['foo-package'],
            self.module)

        self.assertIsInstance(installed_pkgs, dict)
        self.assertIsInstance(installed_pkgs['foo-package.x86_64'], cppkg.PackageDetails)
        self.assertEqual(installed_pkgs['foo-package.x86_64'].name, 'foo-package')
        self.assertEqual(installed_pkgs['foo-package.x86_64'].arch, 'x86_64')
        self.assertEqual(installed_pkgs['foo-package.x86_64'].version, '6.1.5')
        self.assertEqual(installed_pkgs['foo-package.x86_64'].release, '1')

        self.module.fail_json.assert_not_called()

        self.module.reset_mock()

    def test_get_installed_pkgs_failure_pkg_missing(self):

        cppkg._get_installed_pkgs(
            installed_stdout=PKG_INSTALLED + '\n',
            packages=['foo-package', 'bar-package'],
            module=self.module
        )

        self.module.fail_json.assert_called_once_with(
            msg="Following packages are not installed ['bar-package']"
        )

        self.module.reset_mock()
