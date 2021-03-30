==================
Validations-common
==================

.. image:: https://governance.openstack.org/tc/badges/validations-common.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

A collection of Ansible roles and playbooks to detect and report potential
issues during deployments.

The validations will help detect issues early in the deployment process and
prevent field engineers from wasting time on misconfiguration or hardware
issues in their environments.

* Free software: Apache_license_
* Documentation: https://docs.openstack.org/validations-common/latest/
* Release notes: https://docs.openstack.org/releasenotes/validations-commons/
* Source: https://opendev.org/openstack/validations-common
* Bugs - Upstream: https://bugs.launchpad.net/tripleo/+bugs?field.tag=validations
* Bugs - Downstream: https://bugzilla.redhat.com/buglist.cgi?component=validations-common&product=Red%20Hat%20OpenStack

Installation
============
Recommended process
-------------------

There are several different ways to install validations-common.
However it is **recommended** to both install and use
the package inside python virtual environment.

At the command line using `pip`.

.. code-block:: console

    $ pip install validations-common


Or, if you have virtualenvwrapper_ installed.

.. code-block:: console

    $ mkvirtualenv validations-common
    $ pip install validations-common

Installation with package manager
---------------------------------
Alternativelly it is possible to install validations-common using package manager.

Such as `yum`...

.. code-block:: console

    $ yum install validations-common


or the more modern `dnf`.

.. code-block:: console

    $ dnf install validations-common


Usage
=====

Once the validations-common project has been installed,
navigate to the chosen share path, usually `/usr/share/ansible`
to access the installed roles, playbooks, and libraries.

While the validations-common can be run by itself,
it nonetheless depends on Ansible and validations-libs.
Therefore it isn't recommended to use only validations-common.

The validations included with validations-common are intended to be demonstrations,
capable of running on most setups. But they are not meant for production environment.

.. _virtualenvwrapper: https://pypi.org/project/virtualenvwrapper/
.. _Apache_license: http://www.apache.org/licenses/LICENSE-2.0


Validations Callbacks
=====================
http_json callback
------------------

The callback `http_json` sends Validations logs and information to an HTTP
server as a JSON format in order to get caught and analysed with external
tools for log parsing (as Fluentd or others).

This callback inherits from `validation_json` the format of the logging
remains the same as the other logger that the Validation Framework is using
by default.

To enable this callback, you need to add it to the callback whitelist.
Then you need to export your http server url and port::

    export HTTP_JSON_SERVER=http://localhost
    export HTTP_JSON_PORT=8989

The callback will post JSON log to the URL provided.
This repository has a simple HTTP server for testing purpose under::

    tools/http_server.py

The default host and port are localhost and 8989, feel free to adjust those
values to your needs.
