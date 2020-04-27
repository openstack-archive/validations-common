==================
http_json callback
==================

The callback http_json sends Validations logs and information to an HTTP
server as a JSON format in order to get caught and analysed with external
tools for log parsing (as Fluentd or others).

This callback inherits from validation_json the format of the logging
remains the same as the other logger that the Validation Framework is using
by default.

To enable this callback, you need to add it to the callback whitelist.
Then you need to export your http server url and port.

.. code-block:: console

    export HTTP_JSON_SERVER=http://localhost
    export HTTP_JSON_PORT=8989

The callback will post JSON log to the URL provided.
This repository has a simple HTTP server for testing purpose under:

.. code-block:: console

    tools/http_server.py

The default host and port are localhost and 8989, feel free to adjust those
values to your needs.
