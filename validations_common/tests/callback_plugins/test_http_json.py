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

from validations_common.tests import base
from validations_common.tests import fakes

import validations_common.library.reportentry as validation
from validations_common.callback_plugins import http_json


class TestHttpJson(base.TestCase):

    def setUp(self):
        super(TestHttpJson, self).setUp()
