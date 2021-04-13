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
test_validation
----------------------------------

Tests for `validation` sub module.

"""
import argparse

from unittest import mock

from validations_common import validation
from validations_common.tests import base


class TestValidationModule(base.TestCase):

    def setUp(self):
        self.module = mock.MagicMock()

        super(TestValidationModule, self).setUp()

    def test_module_init(self):
        """Check for presence of required module attributes.
        Including the color constants needed for output formatting.
        """
        required_attributes = [
            'DESCRIPTION',
            'EPILOG',
            'RED',
            'GREEN',
            'CYAN',
            'RESET'
        ]

        module_attributes = set(dir(validation))

        self.assertTrue(set(required_attributes).issubset(module_attributes))


class TestCommaListGroupAction(base.TestCase):

    def setUp(self):
        super(TestCommaListGroupAction, self).setUp()

    @mock.patch('validations_common.validation.setattr')
    def test_comma_list_group_action(self, mock_setattr):
        """As there is not much to test in this class
        the assertions are made on attributes and inheritance.
        """
        action = validation._CommaListGroupAction(
            dest='foo',
            option_strings='')

        action('foo', 'bar', 'fizz,buzz')

        self.assertEqual(type(action).__mro__[1], argparse.Action)
        self.assertEqual(action.dest, 'foo')
        self.assertEqual(action.option_strings, '')
        mock_setattr.assert_called_once_with('bar', 'foo', ['fizz', 'buzz'])


class TestCommaListAction(base.TestCase):

    def setUp(self):
        super(TestCommaListAction, self).setUp()

    @mock.patch('validations_common.validation.setattr')
    def test_comma_list_action(self, mock_setattr):
        """As there is not much to test in this class
        the assertions are made on attributes and inheritance.
        """
        action = validation._CommaListAction(
            dest='foo',
            option_strings='')

        action('foo', 'bar', 'fizz,buzz')

        self.assertEqual(type(action).__mro__[1], argparse.Action)
        self.assertEqual(action.dest, 'foo')
        self.assertEqual(action.option_strings, '')
        mock_setattr.assert_called_once_with('bar', 'foo', ['fizz', 'buzz'])


class TestValidation(base.TestCase):

    def setUp(self):
        super(TestValidation, self).setUp()

    def test_validation_init(self):
        pass

    def test_validation_parser(self):
        pass

    def test_validation_print_dict_table(self):
        pass

    def test_validation_print_tuple_table(self):
        pass

    def test_validation_write_output(self):
        pass

    def test_validation_take_action_run(self):
        pass

    def test_validation_take_action_list(self):
        pass

    def test_validation_take_action_show(self):
        pass
