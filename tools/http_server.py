#!/usr/bin/env python3
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
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


class SimpleHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("Received GET request:\n"
                     "Headers: {}\n".format(str(self.headers)))
        self._set_headers()
        self.wfile.write("GET request: {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        logging.info("Received POST request:\n"
                     "Headers: {}\n"
                     "Body: \n{}\n".format(self.headers, data.decode('utf-8')))
        self._set_headers()
        self.wfile.write("POST request: {}".format(self.path).encode('utf-8'))


def run(host='localhost', port=8989):
    logging.basicConfig(level=logging.INFO)
    http_server = HTTPServer((host, port), SimpleHandler)
    logging.info("Starting http server...\n")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    http_server.server_close()
    logging.info('Stopping http server...\n')


if __name__ == '__main__':
    run()
