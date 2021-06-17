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
test_fail_if_no_hosts
----------------------------------

Tests for `fail_if_no_hosts` callback plugin.

"""
try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

from validations_common.callback_plugins import fail_if_no_hosts

from ansible.plugins.callback import CallbackBase


class TestFailIfNoHosts(base.TestCase):
    def setUp(self):
        super(TestFailIfNoHosts, self).setUp()

    def test_callback_instantiation(self):
        """
        Verifying that the CallbackModule is instantiated properly.

        Test checks presence of CallbackBase in the inheritance chain,
        in order to ensure that
        """
        callback = fail_if_no_hosts.CallbackModule()

        self.assertEqual(type(callback).__mro__[1], CallbackBase)

        self.assertIn('CALLBACK_NAME', dir(callback))
        self.assertIn('CALLBACK_VERSION', dir(callback))

        self.assertEqual(callback.CALLBACK_NAME, 'fail_if_no_hosts')
        self.assertIsInstance(callback.CALLBACK_VERSION, float)

    @mock.patch('sys.exit', autospec=True)
    def test_callback_playbook_on_stats_no_hosts(self, mock_exit):
        """
        Following test concerns stats, an instance of AggregateStats
        and how it's processed by the callback.

        When the v2_playbook_on_stats method of the callback is called,
        a number of hosts in the stats.processed dictionary is checked.
        If there are no hosts in the stats.processed dictionary,
        the callback calls sys.exit.
        """
        callback = fail_if_no_hosts.CallbackModule()
        stats = mock.MagicMock()

        callback.v2_playbook_on_stats(stats)
        mock_exit.assert_called_once_with(10)

    @mock.patch('sys.exit', autospec=True)
    def test_callback_playbook_on_stats_some_hosts(self, mock_exit):
        """
        Following test concerns stats, an instance of AggregateStats
        and how it's processed by the callback.

        When the v2_playbook_on_stats method of the callback is called,
        a number of hosts in the stats.processed dictionary is checked.
        If there are hosts in the stats.processed dictionary,
        sys.exit is never called.
        """

        callback = fail_if_no_hosts.CallbackModule()
        stats = mock.MagicMock()

        stats.processed = {
            'system_foo': 'foo',
            'system_bar': 'bar'}

        callback.v2_playbook_on_stats(stats)
        mock_exit.assert_not_called()
