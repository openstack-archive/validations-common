# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__metaclass__ = type

import datetime
import os

from functools import reduce
from ansible.plugins.callback import CallbackBase

DOCUMENTATION = '''
    callback: stdout
    short_description: Ansible screen output as JSON file
    version_added: "1.0"
    description: This callback prints simplify Ansible information to the
        console.
    type: stdout
    requirements: None
'''


def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()


def secondsToStr(t):
    def rediv(ll, b):
        return list(divmod(ll[0], b)) + ll[1:]

    return "%d:%02d:%02d.%03d" % tuple(
        reduce(rediv, [[
            t * 1000,
        ], 1000, 60, 60]))


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'validation_stdout'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)
        self.env = {}
        self.start_time = None
        self.current_time = current_time()

    def _new_play(self, play):
        return {
            'play': {
                'host': play.get_name(),
                'validation_id': self.env['playbook_name'],
                'validation_path': self.env['playbook_path'],
                'id': (os.getenv('ANSIBLE_UUID') if os.getenv('ANSIBLE_UUID')
                       else str(play._uuid)),
                'duration': {
                    'start': current_time()
                }
            },
            'tasks': []
        }

    def _new_task(self, task):
        return {
            'task': {
                'name': task.get_name(),
                'id': str(task._uuid),
                'duration': {
                    'start': current_time()
                }
            },
            'hosts': {}
        }

    def _val_task(self, task_name):
        return {
            'task': {
                'name': task_name,
                'hosts': {}
            }
        }

    def _val_task_host(self, task_name):
        return {
            'task': {
                'name': task_name,
                'hosts': {}
            }
        }
