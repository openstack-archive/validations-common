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
test_validation_output
----------------------------------

Tests for `validation_output` callback plugin.

"""
try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

from ansible.plugins.callback import CallbackBase

from validations_common.callback_plugins import validation_output


class MockStats(mock.MagicMock):
    """
    MockStats mimics some behavior of the ansible.executor.stats.AggregateStats.
    Othewise it behaves like an ordinary MagicMock
    """
    summary = {}

    def summarize(self, anything):
        return self.summary.get(anything, self.summary)


class DummyResults(dict):
    """
    DummyResults is used in tests as a substitute, mimicking the behavior
    of the ansible.executor.task_results.TaskResults class.
    """
    def __init__(self):
        self.task_fields = {}


class TestValidationOutput(base.TestCase):
    def setUp(self):
        super(TestValidationOutput, self).setUp()
        self.module = mock.MagicMock()

    def test_callback_instantiation(self):
        """
        Verifying that the CallbackModule is instantiated properly.
        Test checks presence of CallbackBase in the inheritance chain,
        in order to ensure that folowing tests are performed with
        the correct assumptions.
        """
        callback = validation_output.CallbackModule()
        self.assertEqual(type(callback).__mro__[1], CallbackBase)
        """
        Every ansible callback needs to define variable with name and version.
        The validation_output plugin also defines CALLBACK_TYPE,
        so we need to check it too.
        """
        self.assertIn('CALLBACK_NAME', dir(callback))
        self.assertIn('CALLBACK_VERSION', dir(callback))
        self.assertIn('CALLBACK_TYPE', dir(callback))
        self.assertEqual(callback.CALLBACK_NAME, 'validation_output')
        self.assertIsInstance(callback.CALLBACK_VERSION, float)
        self.assertEqual(callback.CALLBACK_TYPE, 'stdout')

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_WARN')
    @mock.patch('pprint.pprint')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.FAILURE_TEMPLATE',
        create=True)
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_print_failure_message_script(self, mock_display,
                                          mock_failure_template, mock_pprint,
                                          mock_color_warn, mock_color_error):
        """
        The test places assertions on the values of arguments passed
        to the format method of the FAILURE_TEMPLATE obj, and the display
        method of the ansible.utils.display.Display class.
        As such it mostly deals with string manipulation, and is therefore
        sensitive to localisation and formatting changes,
        including the color of the output text.
        """
        mock_abridged_result = mock.MagicMock()
        mock_results = DummyResults()
        mock_results._task_fields = {
            'action': 'script',
            'args': '_raw_params'
        }

        host_name = 'foo'
        task_name = 'bar'
        mock_results['results'] = [
            {
                'foo': 'bar',
                'failed': 5
            }
        ]

        mock_results['rc'] = 'fizz'
        mock_results['invocation'] = {
            'module_args': {
                '_raw_params': 'buzz'
            },

        }

        callback = validation_output.CallbackModule()

        callback.print_failure_message(
            host_name,
            task_name,
            mock_results,
            mock_abridged_result
        )

        mock_failure_template.format.assert_called_once_with(
            task_name,
            host_name,
            'Script `buzz` exited with code: fizz'
        )

        mock_display.assert_called_once_with(
            mock_failure_template.format(),
            color=mock_color_error
        )

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_WARN')
    @mock.patch('pprint.pprint')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.FAILURE_TEMPLATE',
        create=True)
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_print_failure_message_rc_and_cmd(self, mock_display,
                                              mock_failure_template,
                                              mock_pprint,
                                              mock_color_warn,
                                              mock_color_error):
        """
        The test places assertions on the values of arguments passed
        to the format method of the FAILURE_TEMPLATE obj, and the display
        method of the ansible.utils.display.Display class.
        As such it mostly deals with string manipulation, and is therefore
        sensitive to localisation and formatting changes,
        including the color of the output text.
        The test assumes that both 'rc' and 'cmd' keys are present
        within the results object.
        """
        mock_abridged_result = mock.MagicMock()

        host_name = 'foo'
        task_name = 'bar'

        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ],
            'cmd': 'fizz',
            'rc': 'buzz'
        }

        callback = validation_output.CallbackModule()

        callback.print_failure_message(
            host_name,
            task_name,
            result_dict,
            mock_abridged_result
        )

        mock_failure_template.format.assert_called_once_with(
            task_name,
            host_name,
            "Command `fizz` exited with code: buzz"
        )

        mock_display.assert_called_once_with(
            mock_failure_template.format(),
            color=mock_color_error
        )

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_WARN')
    @mock.patch('pprint.pprint')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.FAILURE_TEMPLATE',
        create=True)
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_print_failure_message_unknown_error_no_warn(self, mock_display,
                                                         mock_failure_template,
                                                         mock_pprint,
                                                         mock_color_warn,
                                                         mock_color_error):
        """
        The test places assertions on the values of arguments passed
        to the format method of the FAILURE_TEMPLATE obj, the display
        method of the ansible.utils.display.Display class
        and the pprint method.
        As such it mostly deals with string manipulation, and is therefore
        sensitive to localisation and formatting changes,
        including the color of the output text.
        Test assumes that neither pair of 'rc' and 'cmd' keys,
        nor the 'msg' key, exists within the results object.
        Therefore an Unknown error is assumed to have occured and
        output is adjusted accordignly.
        Furthermore, the test assumes that in absence of 'warnings' key,
        no warnings will be passed to the display method.
        """
        mock_abridged_result = mock.MagicMock()

        host_name = 'foo'
        task_name = 'bar'

        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ]
        }

        callback = validation_output.CallbackModule()

        callback.print_failure_message(
            host_name,
            task_name,
            result_dict,
            mock_abridged_result
        )

        mock_failure_template.format.assert_called_once_with(
            task_name,
            host_name,
            "Unknown error"
        )

        mock_display.assert_called_once_with(
            mock_failure_template.format(),
            color=mock_color_error
        )

        mock_pprint.assert_called_once_with(
            mock_abridged_result,
            indent=4)

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_WARN')
    @mock.patch('pprint.pprint')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.FAILURE_TEMPLATE',
        create=True)
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_print_failure_message_unknown_error_warn(self, mock_display,
                                                      mock_failure_template,
                                                      mock_pprint,
                                                      mock_color_warn,
                                                      mock_color_error):
        """
        The test places assertions on the values of arguments passed
        to the format method of the FAILURE_TEMPLATE obj, the display
        method of the ansible.utils.display.Display class
        and the pprint method.
        As such it mostly deals with string manipulation, and is therefore
        sensitive to localisation and formatting changes,
        including the color of the output text.
        Test assumes that neither pair of 'rc' and 'cmd' keys,
        nor the 'msg' key, exists within the results object.
        Therefore an Unknown error is assumed to have occured and
        output is adjusted accordignly.
        Furthermore, the test assumes that when the 'warnings' key is present,
        the display method will be called with list entries as arguments.
        """
        mock_abridged_result = mock.MagicMock()

        host_name = 'foo'
        task_name = 'bar'

        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ],
            'warnings': [
                'foo'
            ]
        }

        callback = validation_output.CallbackModule()

        callback.print_failure_message(
            host_name,
            task_name,
            result_dict,
            mock_abridged_result)

        mock_failure_template.format.assert_called_once_with(
            task_name,
            host_name,
            "Unknown error")

        mock_display.assert_has_calls(
            [
                mock.call(
                    mock_failure_template.format(),
                    color=mock_color_error
                ),
                mock.call(
                    "* foo ",
                    color=mock_color_warn
                )
            ]
        )

        mock_pprint.assert_called_once_with(
            mock_abridged_result,
            indent=4)

    @mock.patch('ansible.constants.COLOR_WARN')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.WARNING_TEMPLATE',
        create=True)
    @mock.patch(
        'validations_common.callback_plugins.validation_output.CallbackModule._dump_results',
        return_value={'foo': 'bar'})
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_v2_runner_on_ok_warnings(self, mock_display, mock_dump_results,
                                      mock_warn_template, mock_error_color):
        """
        The test asserts on argumets passed to print_failure_message method.
        In order to check the call arguments we need
        initialize them before passing the mock_results to the tested method.
        It is a bit hacky, but the most simple way I know how to make sure
        the relevant mocks ids don't change.
        If you know how to improve it, go for it.
        """
        mock_results = mock.MagicMock()
        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ],
            'warnings': [
                'foo'
            ]
        }

        mock_results._result = result_dict
        mock_results._host()
        mock_results._task.get_name()
        mock_results._task_fields()

        callback = validation_output.CallbackModule()

        callback.v2_runner_on_ok(mock_results)

        mock_dump_results.assert_called_once_with(result_dict)
        mock_warn_template.format.assert_called_once_with(
            mock_results._task.get_name(),
            mock_results._host,
            'foo\n')
        mock_display.assert_called_once_with(
            mock_warn_template.format(),
            color=mock_error_color)

    @mock.patch('ansible.constants.COLOR_OK')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.DEBUG_TEMPLATE',
        create=True)
    @mock.patch(
        'validations_common.callback_plugins.validation_output.CallbackModule._dump_results',
        return_value={'foo': 'bar'})
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_v2_runner_on_ok_debug_vars(self, mock_display, mock_dump_results,
                                        mock_debug_template, mock_ok_color):
        """
        The test asserts on argumets passed to print_failure_message method.
        In order to check the call arguments we need
        initialize them before passing the mock_results to the tested method.
        It is a bit hacky, but the most simple way I know how to make sure
        the relevant mocks ids don't change.
        If you know how to improve it, go for it.
        """
        mock_results = mock.MagicMock()
        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ],
            'fizz': 'buzz'
        }

        mock_results._result = result_dict
        mock_results._host()
        mock_results._task.get_name()
        mock_results._task_fields = {
            'action': 'debug',
            'args': {'var': 'fizz'}
        }

        callback = validation_output.CallbackModule()

        callback.v2_runner_on_ok(mock_results)

        mock_dump_results.assert_called_once_with(result_dict)

        mock_debug_template.format.assert_called_once_with(
            mock_results._host,
            "fizz: buzz"
        )
        mock_display.assert_called_once_with(
            mock_debug_template.format(),
            color=mock_ok_color)

    @mock.patch('ansible.constants.COLOR_OK')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.DEBUG_TEMPLATE',
        create=True)
    @mock.patch(
        'validations_common.callback_plugins.validation_output.CallbackModule._dump_results',
        return_value={'foo': 'bar'})
    @mock.patch(
        'ansible.utils.display.Display.display',
        create=True)
    def test_v2_runner_on_ok_debug_msg(self, mock_display, mock_dump_results,
                                       mock_debug_template, mock_ok_color):
        """
        The test asserts on argumets passed to print_failure_message method.
        In order to check the call arguments we need
        initialize them before passing the mock_results to the tested method.
        It is a bit hacky, but the most simple way I know how to make sure
        the relevant mocks ids don't change.
        If you know how to improve it, go for it.
        """
        mock_results = mock.MagicMock()
        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ]
        }

        mock_results._result = result_dict
        mock_results._host()
        mock_results._task.get_name()
        mock_results._task_fields = {
            'action': 'debug',
            'args': {'msg': 'fizz'}
        }

        callback = validation_output.CallbackModule()

        callback.v2_runner_on_ok(mock_results)

        mock_dump_results.assert_called_once_with(result_dict)

        mock_debug_template.format.assert_called_once_with(
            mock_results._host,
            "Message: fizz"
        )
        mock_display.assert_called_once_with(
            mock_debug_template.format(),
            color=mock_ok_color)

    @mock.patch(
        'validations_common.callback_plugins.validation_output.CallbackModule._dump_results',
        return_value={'foo': 'bar'})
    @mock.patch('validations_common.callback_plugins.validation_output.CallbackModule.print_failure_message')
    def test_v2_runner_on_failed_one_result(self, mock_print, mock_dump_results):
        """
        The test asserts on argumets passed to print_failure_message method.
        In order to check the call arguments we need
        initialize them before passing the mock_results to the tested method.
        It is a bit hacky, but the most simple way I know how to make sure
        the relevant mocks ids don't change.
        If you know how to improve it, go for it.
        """
        mock_results = mock.MagicMock()
        result_dict = {
            'results': [
                {
                    'foo': 'bar',
                    'failed': 5
                }
            ]
        }

        mock_results._result = result_dict
        mock_results._host()
        mock_results._task.get_name()

        callback = validation_output.CallbackModule()

        callback.v2_runner_on_failed(mock_results)

        mock_print.assert_called_once_with(
            mock_results._host,
            mock_results._task.get_name(),
            {
                'foo': 'bar',
                'failed': 5
            },
            {
                'foo': 'bar',
                'failed': 5
            }
        )

    @mock.patch(
        'validations_common.callback_plugins.validation_output.CallbackModule._dump_results',
        return_value={'foo': 'bar'})
    @mock.patch('validations_common.callback_plugins.validation_output.CallbackModule.print_failure_message')
    def test_v2_runner_on_failed_no_result(self, mock_print, mock_dump_results):
        """
        The test asserts on argumets passed to print_failure_message method.
        In order to check the call arguments we need
        initialize them before passing the mock_results to the tested method.
        It is a bit hacky, but the most simple way I know how to make sure
        the relevant mocks ids don't change.
        If you know how to improve it, go for it.
        """
        mock_results = mock.MagicMock()
        result_dict = {}

        mock_results._result = result_dict
        mock_results._host()
        mock_results._task.get_name()

        callback = validation_output.CallbackModule()

        callback.v2_runner_on_failed(mock_results)

        mock_print.assert_called_once_with(
            mock_results._host,
            mock_results._task.get_name(),
            {},
            {
                'foo': 'bar'
            }
        )

    @mock.patch('validations_common.callback_plugins.validation_output.CallbackModule.print_failure_message')
    def test_v2_runner_on_unreachable(self, mock_print):
        """
        The test asserts on argumets passed to print_failure_message method.
        In order to check the call arguments we need
        initialize them before passing the mock_results to the tested method.
        It is a bit hacky, but the most simple way I know how to make sure
        the relevant mocks ids don't change.
        If you know how to improve it, go for it.
        """
        mock_results = mock.MagicMock()
        results_dict = {'msg': 'The host is unreachable.'}

        mock_results._host()
        mock_results._task.get_name()

        callback = validation_output.CallbackModule()

        callback.v2_runner_on_unreachable(mock_results)

        mock_print.assert_called_once_with(
            mock_results._host,
            mock_results._task.get_name(),
            results_dict,
            results_dict)

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_OK')
    @mock.patch('validations_common.callback_plugins.validation_output.print')
    @mock.patch.object(CallbackBase, '_display.display', create=True)
    def test_v2_playbook_on_stats_no_hosts(self, mock_display, mock_print,
                                           mock_color_ok, mock_color_error):
        """
        In case we don't supply any hosts, we expect the method not to call
        display or related methods and attributes even once.
        The final call to print function is not an ideal place for assertion,
        as the string might get localised and/or adjusted in the future.
        """
        callback = validation_output.CallbackModule()
        dummy_stats = mock.MagicMock()

        callback.v2_playbook_on_stats(dummy_stats)

        mock_color_ok.assert_not_called()
        mock_color_error.assert_not_called()
        mock_display.assert_not_called()
        mock_print.assert_called_once()

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_OK')
    @mock.patch('validations_common.callback_plugins.validation_output.print')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.sorted',
        return_value=['bar', 'foo'])
    @mock.patch('ansible.utils.display.Display.display')
    @mock.patch('ansible.plugins.callback.CallbackBase')
    def test_v2_playbook_on_stats_no_fail(self, mock_callback_base,
                                          mock_display, mock_sorted,
                                          mock_print, mock_color_ok,
                                          mock_color_error):
        """
        When we have hosts and their state is not specified,
        we expect them to be considered a `pass` and the display method
        to be called with appropriate arguments.
        The final call to print function is not an ideal place for assertion,
        as the string might get localised and/or adjusted in the future.
        """
        callback = validation_output.CallbackModule()
        dummy_stats = MockStats()
        callback.v2_playbook_on_stats(dummy_stats)

        mock_display.assert_called_with('* foo', color=mock_color_ok)
        mock_print.assert_called_once()

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_OK')
    @mock.patch('validations_common.callback_plugins.validation_output.print')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.sorted',
        return_value=['bar', 'buzz', 'fizz', 'foo'])
    @mock.patch('ansible.utils.display.Display.display')
    @mock.patch('ansible.plugins.callback.CallbackBase')
    def test_v2_playbook_on_stats_some_fail(self, mock_callback_base,
                                            mock_display, mock_sorted,
                                            mock_print, mock_color_ok,
                                            mock_color_error):
        """
        When at least one host is specified as failure and/or unreachable
        we expect it to be considered a `failure` and the display method
        to be called with the appropriate arguments in the proper order.
        The final call to print function is not an ideal place for assertion,
        as the string might get localised and/or adjusted in the future.
        """

        callback = validation_output.CallbackModule()
        dummy_stats = MockStats()
        dummy_stats.summary = {
            'fizz': {
                'failures': 5
            }
        }
        expected_calls = [
            mock.call('* fizz', color=mock_color_error),
            mock.call('* bar', color=mock_color_ok),
            mock.call('* buzz', color=mock_color_ok),
            mock.call('* foo', color=mock_color_ok)
        ]

        callback.v2_playbook_on_stats(dummy_stats)

        mock_display.assert_has_calls(expected_calls)
        mock_print.assert_called()

    @mock.patch('ansible.constants.COLOR_ERROR')
    @mock.patch('ansible.constants.COLOR_OK')
    @mock.patch('validations_common.callback_plugins.validation_output.print')
    @mock.patch(
        'validations_common.callback_plugins.validation_output.sorted',
        return_value=['bar', 'buzz', 'fizz', 'foo'])
    @mock.patch('ansible.utils.display.Display.display')
    @mock.patch('ansible.plugins.callback.CallbackBase')
    def test_v2_playbook_on_stats_all_fail(self, mock_callback_base,
                                           mock_display, mock_sorted,
                                           mock_print, mock_color_ok,
                                           mock_color_error):
        """
        When at all hosts are specified as failure and/or unreachable
        we expect them to be considered a `failure` and the display method
        to be called with the appropriate arguments in the proper order.
        The final call to print function is not an ideal place for assertion,
        as the string might get localised and/or adjusted in the future.
        """

        callback = validation_output.CallbackModule()
        dummy_stats = MockStats()

        dummy_stats.summary = {
            'fizz': {
                'failures': 5
            },
            'foo': {
                'failures': 5
            },
            'bar': {
                'failures': 5
            },
            'buzz': {
                'failures': 5
            }
        }

        expected_calls = [
            mock.call('* bar', color=mock_color_error),
            mock.call('* buzz', color=mock_color_error),
            mock.call('* fizz', color=mock_color_error),
            mock.call('* foo', color=mock_color_error)
        ]

        callback.v2_playbook_on_stats(dummy_stats)

        mock_display.assert_has_calls(expected_calls)
        mock_print.assert_called()
