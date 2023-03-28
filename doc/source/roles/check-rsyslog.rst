================
check_rsyslog
================

--------------
About The Role
--------------

An Ansible role which detects package presence and running service on the target host
and fails if it doesn't find it.

Requirements
============

No requirements.

Dependencies
============

No dependencies.

Example Playbook
================

.. code-block:: yaml

   - hosts: localhost
     gather_facts: true
     roles:
       - check_rsyslog

License
=======

Apache

Author Information
==================

**Red Hat TripleO DFG:DF Squad:VF**

----------------
Full Description
----------------

.. ansibleautoplugin::
   :role: validations_common/roles/check_rsyslog
