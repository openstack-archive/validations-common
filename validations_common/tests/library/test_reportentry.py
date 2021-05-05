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
test_report_entry
----------------------------------

Tests for `reportentry` module.
"""

try:
    from unittest import mock
except ImportError:
    import mock

from validations_common.tests import base
from validations_common.tests import fakes

import validations_common.library.reportentry as validation


reason = "Reason #1"
recommendation = ['Recommendation #1']
recommendations = [
    'Recommendation #1', 'Recommendation #2', 'Recommendation #3'
]
valid_report = '''[{}] '{}'
 - RECOMMENDATION: Recommendation #1
'''

multi_reco_valid_report = '''[{}] '{}'
 - RECOMMENDATION: Recommendation #1
 - RECOMMENDATION: Recommendation #2
 - RECOMMENDATION: Recommendation #3
'''


class TestReportEntry(base.TestCase):
    def setUp(self):
        super(TestReportEntry, self).setUp()
        self.module = mock.MagicMock()

    def test_format_msg_report_error(self):
        '''Test reportentry with error status'''

        status = "ERROR"
        one_reco_report = valid_report.format(status, reason, recommendation)
        report = validation.format_msg_report(status, reason, recommendation)
        validation.display_type_report(self.module, status, report)
        self.assertEqual(one_reco_report, report)
        validation.display_type_report(self.module, status, report)
        self.module.fail_json.assert_called_with(msg=report)

    def test_format_msg_report_skipped(self):
        '''Test reportentry with skipped status'''

        status = "SKIPPED"
        one_reco_report = valid_report.format(status, reason, recommendation)
        report = validation.format_msg_report(status, reason, recommendation)
        self.assertEqual(one_reco_report, report)

        validation.display_type_report(self.module, status, report)
        self.module.exit_json.assert_called_with(changed=False,
                                                 warnings=report)

    def test_format_msg_report_with_multiple_reco(self):
        '''Test reportentry with multiple recommendation'''

        status = "OK"
        multi_reco_report = \
            multi_reco_valid_report.format(status,
                                           reason,
                                           recommendations)
        report = validation.format_msg_report(status, reason, recommendations)
        self.assertEqual(multi_reco_report, report)

        validation.display_type_report(self.module, status, report)
        self.module.exit_json.assert_called_with(changed=False, msg=report)
