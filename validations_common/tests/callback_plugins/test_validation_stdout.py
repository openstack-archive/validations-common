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
test_validation_stdout
----------------------------------

Tests for `validation_stdout` callback plugin.

"""
import re

try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

from validations_common.callback_plugins import validation_stdout

from ansible.plugins.callback import CallbackBase


def is_iso_time(time_string):
    """
    Checks if string represents valid time in ISO format,
    with the default delimiter.
    Regex is somewhat convoluted, but general enough to last
    at least until the 9999 AD.

    Returns:
        True if string matches the pattern.
        False otherwise.
    """
    match = re.match(
        r'\d{4}-[01][0-9]-[0-3][0-9]T[0-3][0-9](:[0-5][0-9]){2}\.\d+Z',
        time_string)

    if match:
        return True
    else:
        return False


class TestValidationStdout(base.TestCase):
    """Tests of validation_stdout callback module.
    """
    def setUp(self):
        super(TestValidationStdout, self).setUp()
        self.module = mock.MagicMock()

    def test_callback_instantiation(self):
        """
        Verifying that the CallbackModule is instantiated properly.
        Test checks presence of CallbackBase in the inheritance chain,
        in order to ensure that folowing tests are performed with
        the correct assumptions.
        """
        callback = validation_stdout.CallbackModule()

        self.assertEqual(type(callback).__mro__[1], CallbackBase)

        """
        Every ansible callback needs to define variable with name and version.
        """
        self.assertIn('CALLBACK_NAME', dir(callback))
        self.assertIn('CALLBACK_VERSION', dir(callback))

        self.assertEqual(callback.CALLBACK_NAME, 'validation_stdout')

        self.assertIsInstance(callback.CALLBACK_VERSION, float)

        """
        Additionally, the 'validation_stdout' callback performs several
        other operations during instantiation.
        """

        self.assertEqual(callback.env, {})
        self.assertIsNone(callback.start_time)
        """
        Callback time sanity check only verifies general format
        of the stored time to be  iso format `YYYY-MM-DD HH:MM:SS.mmmmmm`
        with 'T' as a separator.
        For example: '2020-07-03T13:28:21.224103Z'
        """
        self.assertTrue(is_iso_time(callback.current_time))

    @mock.patch(
        'ansible.playbook.play.Play._uuid',
        autospec=True,
        return_value='bar')
    @mock.patch(
        'ansible.playbook.play.Play.get_name',
        autospec=True,
        return_value='foo')
    @mock.patch('ansible.playbook.play.Play')
    def test_new_play(self, mock_play, mock_play_name, mock_play_uuid):
        """
        From the callback point of view,
        both Play and Task are virtually identical.
        Test involving them are therefore also very similar.
        """
        callback = validation_stdout.CallbackModule()
        callback.env['playbook_name'] = 'fizz'
        callback.env['playbook_path'] = 'buzz/fizz'

        play_dict = callback._new_play(mock_play)

        mock_play_name.assert_called_once()
        mock_play_uuid.assert_called_once()

        """
        Callback time sanity check only verifies general format
        of the stored time to be  iso format `YYYY-MM-DD HH:MM:SS.mmmmmm`
        with 'T' as a separator.
        For example: '2020-07-03T13:28:21.224103Z'
        """
        self.assertTrue(is_iso_time(play_dict['play']['duration']['start']))

        self.assertEqual('fizz', play_dict['play']['validation_id'])
        self.assertEqual('buzz/fizz', play_dict['play']['validation_path'])

    @mock.patch(
        'ansible.playbook.task.Task._uuid',
        autospec=True,
        return_value='bar')
    @mock.patch(
        'ansible.playbook.task.Task.get_name',
        autospec=True,
        return_value='foo')
    @mock.patch('ansible.playbook.task.Task')
    def test_new_task(self, mock_task, mock_task_name, mock_task_uuid):
        """
        From the callback point of view,
        both Play and Task are virtually identical.
        Test involving them are therefore also very similar.
        """
        callback = validation_stdout.CallbackModule()
        task_dict = callback._new_task(mock_task)

        mock_task_name.assert_called_once()
        mock_task_uuid.assert_called_once()

        """
        Callback time sanity check only verifies general format
        of the stored time to be  iso format `YYYY-MM-DD HH:MM:SS.mmmmmm`
        with 'T' as a separator.
        For example: '2020-07-03T13:28:21.224103Z'
        """
        self.assertTrue(is_iso_time(task_dict['task']['duration']['start']))

    def test_val_task(self):
        """
        _val_task and _val_task_host methods are virtually identical.
        Their tests are too.
        """
        task_name = 'foo'
        expected_dict = {
            'task': {
                'name': task_name,
                'hosts': {}
            }
        }
        callback = validation_stdout.CallbackModule()

        self.assertEqual(
            expected_dict,
            callback._val_task(task_name=task_name))

    def test_val_task_host(self):
        """
        _val_task and _val_task_host methods are virtually identical.
        Their tests are too.
        """
        task_name = 'foo'
        expected_dict = {
            'task': {
                'name': task_name,
                'hosts': {}
            }
        }
        callback = validation_stdout.CallbackModule()

        self.assertEqual(
            expected_dict,
            callback._val_task_host(task_name=task_name))
