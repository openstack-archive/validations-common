===
dns
===

--------------
About The Role
--------------

An Ansible role to verify that the DNS resolution works.

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
       server_to_lookup: example.com
     roles:
       - dns

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
   :role: validations_common/roles/dns
