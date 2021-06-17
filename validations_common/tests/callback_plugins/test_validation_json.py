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
test_validation_json
----------------------------------

Tests for `validation_json` callback plugin.

"""
import re

try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

from ansible.executor.stats import AggregateStats
from ansible.parsing.ajson import AnsibleJSONEncoder
from ansible.playbook import Playbook
from ansible.plugins.callback import CallbackBase

from validations_common.callback_plugins import validation_json


def is_iso_time(time_string):
    """
    Checks if string represents valid time in ISO format,
    with the default delimiter.
    Regex is somewhat convoluted, but general enough to last
    at least until the 9999 AD.

    :returns:
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


class TestValidationJson(base.TestCase):
    def setUp(self):
        super(TestValidationJson, self).setUp()
        self.module = mock.MagicMock()

    def test_callback_instantiation(self):
        """
        Verifying that the CallbackModule is instantiated properly.
        Test checks presence of CallbackBase in the inheritance chain,
        in order to ensure that folowing tests are performed with
        the correct assumptions.
        """
        callback = validation_json.CallbackModule()
        self.assertEqual(type(callback).__mro__[1], CallbackBase)
        """
        Every ansible callback needs to define variable with name and version.
        The validation_json plugin also defines CALLBACK_TYPE,
        so we need to check it too.
        """
        self.assertIn('CALLBACK_NAME', dir(callback))
        self.assertIn('CALLBACK_VERSION', dir(callback))
        self.assertIn('CALLBACK_TYPE', dir(callback))
        self.assertEqual(callback.CALLBACK_NAME, 'validation_json')
        self.assertIsInstance(callback.CALLBACK_VERSION, float)
        self.assertEqual(callback.CALLBACK_TYPE, 'aggregate')
        """
        Additionally, the 'validation_json' callback performs several
        other operations during instantiation.
        """
        self.assertEqual(callback.results, [])
        self.assertEqual(callback.simple_results, [])
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
        callback = validation_json.CallbackModule()
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
        callback = validation_json.CallbackModule()
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
        callback = validation_json.CallbackModule()
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
        callback = validation_json.CallbackModule()
        self.assertEqual(
            expected_dict,
            callback._val_task_host(task_name=task_name))

    @mock.patch('os.path.basename',
                autospec=True,
                return_value='foo.yaml')
    @mock.patch('os.path.splitext',
                autospec=True,
                return_value=['foo', '.yaml'])
    @mock.patch('ansible.parsing.dataloader.DataLoader', autospec=True)
    def test_v2_playbook_on_start(self, mock_loader,
                                  mock_path_splitext, mock_path_basename):

        callback = validation_json.CallbackModule()
        dummy_playbook = Playbook(mock_loader)
        dummy_playbook._basedir = '/bar'
        dummy_playbook._file_name = '/bar/foo.yaml'

        callback.v2_playbook_on_start(dummy_playbook)

        mock_path_basename.assert_called_once_with('/bar/foo.yaml')
        mock_path_splitext.assert_called_once_with('foo.yaml')

        self.assertEqual('foo', callback.env['playbook_name'])
        self.assertEqual('/bar', callback.env['playbook_path'])

    @mock.patch(
        'validations_common.callback_plugins.validation_json.CallbackModule._new_play',
        autospec=True,
        return_value={'play': {'host': 'foo'}})
    @mock.patch('ansible.playbook.play.Play', autospec=True)
    def test_v2_playbook_on_play_start(self, mock_play, mock_new_play):
        callback = validation_json.CallbackModule()
        callback.v2_playbook_on_play_start(mock_play)

        self.assertIn({'play': {'host': 'foo'}}, callback.results)

    @mock.patch(
        'validations_common.callback_plugins.validation_json.CallbackModule._new_task',
        autospec=True,
        return_value={'task': {'host': 'foo'}})
    @mock.patch('ansible.playbook.task.Task', autospec=True)
    def test_v2_playbook_on_task_start(self, mock_task, mock_new_task):
        """
        CallbackModule methods v2_playbook_on_task_start
        and v2_playbook_on_handler_task_start are virtually identical.
        The only exception being is_conditional parameter
        of the v2_playbook_on_task_start, which isn't used by the method
        at all.
        Therefore both of their tests share documentation.
        In order to verify methods functionality we first append
        a dummy result at the end of CallbackModule.result list.
        Simple dictionary is more than sufficient.
        """
        callback = validation_json.CallbackModule()
        callback.results.append(
            {
                'fizz': 'buzz',
                'tasks': []
            })
        callback.v2_playbook_on_task_start(mock_task, False)
        """
        First we verify that CallbackModule._new_task method was indeed
        called with supplied arguments.
        Afterwards we verify that the supplied dummy task is present
        in first (and in our case only) element of CallbackModule.result list.
        """
        mock_new_task.assert_called_once_with(callback, mock_task)
        self.assertIn({'task': {'host': 'foo'}}, callback.results[0]['tasks'])

    @mock.patch(
        'validations_common.callback_plugins.validation_json.CallbackModule._new_task',
        autospec=True,
        return_value={'task': {'host': 'foo'}})
    @mock.patch('ansible.playbook.task.Task', autospec=True)
    def test_v2_playbook_on_handler_task_start(self, mock_task, mock_new_task):
        """
        CallbackModule methods v2_playbook_on_task_start
        and v2_playbook_on_handler_task_start are virtually identical.
        The only exception being is_conditional parameter
        of the v2_playbook_on_task_start, which isn't used by the method
        at all.
        Therefore both of their tests share documentation.
        In order to verify methods functionality we first append
        a dummy result at the end of CallbackModule.result list.
        Simple dictionary is more than sufficient.
        """
        callback = validation_json.CallbackModule()
        callback.results.append(
            {
                'fizz': 'buzz',
                'tasks': []
            })
        callback.v2_playbook_on_handler_task_start(mock_task)
        """
        First we verify that CallbackModule._new_task method was indeed
        called with supplied arguments.
        Afterwards we verify that the supplied dummy task is present
        in first (and in our case only) element of CallbackModule.result list.
        """
        mock_new_task.assert_called_once_with(callback, mock_task)
        self.assertIn({'task': {'host': 'foo'}}, callback.results[0]['tasks'])

    @mock.patch('json.dumps', return_value='json_dump_foo')
    @mock.patch(
        'validations_common.callback_plugins.validation_json.open',
        create=True)
    def test_v2_playbook_on_stats(self, mock_open,
                                  mock_json_dumps):

        results = [
            {
                'play': {
                    'id': 'fizz'
                }
            }
        ]

        validation_json.VALIDATIONS_LOG_DIR = '/home/foo/validations'

        callback = validation_json.CallbackModule()
        dummy_stats = AggregateStats()

        callback.results = results
        callback.simple_results = results
        callback.env['playbook_name'] = 'foo'
        callback.current_time = 'foo-bar-fooTfoo:bar:foo.fizz'

        dummy_stats.processed['foohost'] = 5

        output = {
            'plays': results,
            'stats': {'foohost': {
                'ok': 0,
                'failures': 0,
                'unreachable': 0,
                'changed': 0,
                'skipped': 0,
                'rescued': 0,
                'ignored': 0}},
            'validation_output': results
        }

        log_file = "{}/{}_{}_{}.json".format(
            "/home/foo/validations",
            'fizz',
            'foo',
            'foo-bar-fooTfoo:bar:foo.fizz')

        kwargs = {
            'cls': AnsibleJSONEncoder,
            'indent': 4,
            'sort_keys': True
        }

        callback.v2_playbook_on_stats(dummy_stats)
        mock_write = mock_open.return_value.__enter__.return_value.write

        mock_open.assert_called_once_with(log_file, 'w')
        mock_json_dumps.assert_called_once_with(output, **kwargs)
        mock_write.assert_called_once_with('json_dump_foo')

    @mock.patch('time.time', return_value=99.99)
    @mock.patch(
        'validations_common.callback_plugins.validation_json.secondsToStr',
        return_value='99.99')
    def test_record_task_result(self, mock_secondsToStr, mock_time):
        """
        Method CallbackModule._record_task_result works mostly with dicts
        and performs few other calls. Therefore the assertions are placed
        on calls to those few functions and the operations performed
        with supplied MagicMock objects.
        """
        mock_on_info = mock.MagicMock()
        mock_result = mock.MagicMock()

        """
        As we have just initialized the callback, we can't expect it to have
        populated properties as the method expects.
        Following lines explicitly set all necessary properties.
        """
        callback_results = [
            {
                'play': {
                    'id': 'fizz',
                    'duration': {}
                },
                'tasks': [
                    {
                        'hosts': {}
                    }
                ]
            }
        ]

        callback_simple_results = [
            {
                'task': {
                    'hosts': {

                    }
                }
            }
        ]

        callback = validation_json.CallbackModule()
        callback.results = callback_results
        callback.simple_results = callback_simple_results
        callback.start_time = 0

        callback._record_task_result(mock_on_info, mock_result)

        mock_time.assert_called()
        mock_secondsToStr.assert_called_once_with(99.99)

        """
        Asserting on set lets us check if the method accessed all expected
        properties of our MagicMock, while also leaving space for
        possible future expansion.
        """
        self.assertGreaterEqual(set(dir(mock_result)), set(['_result', '_host', '_task']))

    @mock.patch(
        'validations_common.callback_plugins.validation_json.CallbackModule._record_task_result',
        autospec=True)
    def test_getattribute_valid_listed(self, mock_record_task_result):
        """
        All of the listed attribute names are checked.
        The __getattribute__ method returns a partial,
        the args supplied to it are stored a tuple.
        """
        listed_names = ['v2_runner_on_ok', 'v2_runner_on_failed',
                        'v2_runner_on_unreachable', 'v2_runner_on_skipped']

        callback = validation_json.CallbackModule()

        for name in listed_names:
            attribute = callback.__getattribute__(name)
            self.assertEqual(
                ({name.split('_')[-1]: True},),
                attribute.args)

    @mock.patch(
        'validations_common.callback_plugins.validation_json.CallbackModule._record_task_result',
        autospec=True)
    def test_getattribute_valid_unlisted(self, mock_record_task_result):
        """
        Since the validation_json.CallbackModule defines it's own
        __getattribute__ method, we can't use `dir` to safely check
        the name of attributes individually,
        as dir itself uses the __getattribute__ method.
        Instead we check if the namespace of the CallbackBase class
        is a subset of validation_json.CallbackModule namespace.
        """
        callback = validation_json.CallbackModule()

        listed_names = set(dir(callback))

        self.assertTrue(listed_names.issuperset(set(dir(CallbackBase))))

    def test_getattribute_invalid(self):
        """
        Attempting to call __getattribute__ method with invalid attribute
        name should result in exception.
        """
        callback = validation_json.CallbackModule()

        fake_names = [name + 'x' for name in [
            'v2_runner_on_ok', 'v2_runner_on_failed',
            'v2_runner_on_unreachable', 'v2_runner_on_skipped']]

        for name in fake_names:
            self.assertRaises(AttributeError, callback.__getattribute__, name)
