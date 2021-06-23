=========
check_cpu
=========

--------------
About The Role
--------------

An Ansible role to check if the Host(s) fit(s) the CPU core requirements

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
     gather_facts: false
     vars:
       minimal_cpu_count: 42
     roles:
       - check_cpu

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
   :role: validations_common/roles/check_cpu
