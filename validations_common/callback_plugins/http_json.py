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

DOCUMENTATION = '''
    requirements:
      - whitelist in configuration
    short_description: sends JSON events to a HTTP server
    description:
      - This plugin logs ansible-playbook and ansible runs to an HTTP server in JSON format
    options:
      server:
        description: remote server that will receive the event
        env:
        - name: HTTP_JSON_SERVER
        default: http://localhost
        ini:
          - section: callback_http_json
            key: http_json_server
      port:
        description: port on which the remote server is listening
        env:
          - name: HTTP_JSON_PORT
        default: 8989
        ini:
          - section: callback_http_json
            key: http_json_port
'''
import datetime
import json
import os

from urllib import request

from validations_common.callback_plugins import validation_json

url = '{}:{}'.format(os.getenv('HTTP_JSON_SERVER', 'http://localhost'),
                     os.getenv('HTTP_JSON_PORT', '8989'))


def http_post(data):
    req = request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    json_data = json.dumps(data)
    json_bytes = json_data.encode('utf-8')
    req.add_header('Content-Length', len(json_bytes))
    response = request.urlopen(req, json_bytes)


def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()


class CallbackModule(validation_json.CallbackModule):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'http_json'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(validation_json.CallbackModule, self).__init__()
        self.results = []
        self.simple_results = []
        self.env = {}
        self.t0 = None
        self.current_time = current_time()

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        http_post({
            'plays': self.results,
            'stats': summary,
            'validation_output': self.simple_results
        })
