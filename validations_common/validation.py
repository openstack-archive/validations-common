#!/usr/bin/env python

#   Copyright 2020 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import argparse
import json
import logging
from prettytable import PrettyTable

from validations_libs.validation_actions import ValidationActions
from validations_libs import constants

DESCRIPTION = "Run, show or list Validations."
EPILOG = "Example: ./validation run --validation check-ftype,512e"
# PrettyTable
RED = "\033[1;31m"
GREEN = "\033[0;32m"
CYAN = "\033[36m"
RESET = "\033[0;0m"


class Validation(argparse.ArgumentParser):
    """Validation client implementation class"""

    log = logging.getLogger(__name__ + ".Validation")

    def __init__(self, description=DESCRIPTION, epilog=EPILOG):
        """Init validation paser"""
        super(Validation, self).__init__(description=DESCRIPTION,
                                         epilog=EPILOG)

    def parser(self, parser):
        """Argument parser for validation"""
        parser.add_argument('action',
                            choices=['run', 'list', 'show'],
                            help='Validation Action')
        parser.add_argument('--inventory', '-i', type=str,
                            help=('Path of the Ansible inventory.'))

        parser.add_argument('--validation', '-v',
                            metavar='<validation_id>[,<validation_id>,...]',
                            dest="validation_name",
                            default=[],
                            help=("Run specific validations, "
                                  "if more than one validation is required "
                                  "separate the names with commas: "
                                  "--validation check-ftype,512e | "
                                  "--validation 512e"))
        parser.add_argument('--group', '-g',
                            metavar='<group>[,<group>,...]',
                            default=[],
                            help=("Run specific group validations, "
                                  "if more than one group is required "
                                  "separate the group names with commas: "
                                  "--group pre-upgrade,prep | "
                                  "--group openshift-on-openstack"))
        parser.add_argument('--quiet', action='store', default=False,
                            help=("Run Ansible in silent mode."))
        parser.add_argument('--validation-dir', dest='validation_dir',
                            default=constants.ANSIBLE_VALIDATION_DIR,
                            help=("Path where the validation playbooks "
                                  "is located."))
        parser.add_argument('--ansible-base-dir', dest='ansible_base_dir',
                            default=constants.DEFAULT_VALIDATIONS_BASEDIR,
                            help=("Path where the ansible roles, library "
                                  "and plugins is located."))
        parser.add_argument('--output-log', dest='output_log',
                            default=None,
                            help=("Path where the run result will be stored"))
        return parser.parse_args()

    def _print_dict_table(self, data):
        """Print table from python dict with PrettyTable"""
        t = PrettyTable(border=True, header=True, padding_width=1)
        # Set Field name by getting the result dict keys
        try:
            t.field_names = data[0].keys()
        except KeyError:
            raise KeyError()
        for r in data:
            if r.get('Status_by_Host'):
                h = []
                for host in r['Status_by_Host'].split(', '):
                    _name, _status = host.split(',')
                    color = (GREEN if _status == 'PASSED' else RED)
                    _name = '{}{}{}'.format(color, _name, RESET)
                    h.append(_name)
                r['Status_by_Host'] = ', '.join(h)
            if r.get('Status'):
                status = r.get('Status')
                color = (CYAN if status in ['starting', 'running']
                         else GREEN if status == 'PASSED' else RED)
                r['Status'] = '{}{}{}'.format(color, status, RESET)
            t.add_row(r.values())
        print(t)

    def _print_tuple_table(self, data, status_col=None):
        """Print table from python Tuple with PrettyTable"""
        if isinstance(data, tuple):
            t = PrettyTable(border=True, header=True, padding_width=1)
            try:
                t.field_names = data[0]
            except KeyError:
                raise KeyError()
            for r in data[1]:
                if status_col:
                    _result = list(r)
                    try:
                        _status = _result[status_col]
                        color = (GREEN if _status == 'PASSED' else RED)
                        _result[status_col] = '{}{}{}'.format(color,
                                                              _status,
                                                              RESET)
                    except ValueError:
                        logging.warning('No status found.')
                    t.add_row(_result)
                else:
                    t.add_row(r)
            print(t)
        else:
            raise RuntimeError("Wrong data type.")

    def _write_output(self, output_log, results):
        """Write output log file as Json format"""
        with open(output_log, 'w') as output:
            output.write(json.dumps({'results': results}, indent=4,
                                    sort_keys=True))

    def take_action(self, parsed_args):
        """Take validation action"""
        # Get parameters:
        action = parsed_args.action
        inventory = parsed_args.inventory
        group = parsed_args.group
        validation_name = parsed_args.validation_name
        quiet = parsed_args.quiet
        validation_dir = parsed_args.validation_dir
        ansible_base_dir = parsed_args.ansible_base_dir

        v_actions = ValidationActions(validation_path=validation_dir,
                                      group=group)
        if 'run' in action:
            results = v_actions.run_validations(
                inventory=inventory,
                group=group,
                validation_name=validation_name,
                base_dir=ansible_base_dir,
                quiet=quiet)
            if results:
                if parsed_args.output_log:
                    self._write_output(parsed_args.output_log, results)
                else:
                    self._print_dict_table(results)
        elif 'list' in action:
            results = v_actions.list_validations()
            if results:
                if parsed_args.output_log:
                    self._write_output(parsed_args.output_log, results)
                else:
                    self._print_tuple_table(results)
        elif 'show' in action:
            results = v_actions.show_history(validation_name)
            if results:
                if parsed_args.output_log:
                    self._write_output(parsed_args.output_log, results)
                else:
                    self._print_tuple_table(data=results, status_col=2)
        else:
            msg = "Unknown Action: {}".format(action)
            raise RuntimeError(msg)

if __name__ == "__main__":
    validation = Validation()
    args = validation.parser(validation)
    validation.take_action(args)
