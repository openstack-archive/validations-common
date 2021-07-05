=========
check_ram
=========

--------------
About The Role
--------------

An Ansible role to check if the Host(s) fit(s) the RAM requirements.

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
       minimal_ram_gb: 42
     roles:
       - check_ram

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
   :role: validations_common/roles/check_ram
