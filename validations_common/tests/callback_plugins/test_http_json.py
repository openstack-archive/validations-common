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
test_http_json
----------------------------------

Tests for `http_json` callback plugin.

"""
try:
    from unittest import mock
except ImportError:
    import mock

import re

from validations_common.tests import base
from validations_common.tests import fakes

from ansible.plugins.callback import CallbackBase

from validations_common.callback_plugins import http_json


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


class TestHttpJson(base.TestCase):

    def setUp(self):
        super(TestHttpJson, self).setUp()

    def test_callback_instantiation(self):
        """
        Verifying that the CallbackModule is instantiated properly.
        Test checks presence of CallbackBase in the inheritance chain,
        in order to ensure that folowing tests are performed with
        the correct assumptions.
        """
        callback = http_json.CallbackModule()

        self.assertEqual(type(callback).__mro__[2], CallbackBase)

        """
        Every ansible callback needs to define variable with name and version.
        """
        self.assertIn('CALLBACK_NAME', dir(callback))
        self.assertIn('CALLBACK_VERSION', dir(callback))
        self.assertIn('CALLBACK_TYPE', dir(callback))

        self.assertEqual(callback.CALLBACK_NAME, 'http_json')

        self.assertIsInstance(callback.CALLBACK_VERSION, float)

        self.assertEqual(callback.CALLBACK_TYPE, 'aggregate')

        """
        Additionally, the 'http_json' callback performs several
        other operations during instantiation.
        """

        self.assertEqual(callback.env, {})
        self.assertIsNone(callback.t0)
        """
        Callback time sanity check only verifies general format
        of the stored time to be  iso format `YYYY-MM-DD HH:MM:SS.mmmmmm`
        with 'T' as a separator.
        For example: '2020-07-03T13:28:21.224103Z'
        """
        self.assertTrue(is_iso_time(callback.current_time))
