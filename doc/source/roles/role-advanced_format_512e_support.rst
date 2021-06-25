============================
advanced_format_512e_support
============================

--------------
About The Role
--------------

An Ansible role to detect whether the node disks use Advanced Format.

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
     roles:
       - advanced_format_512e_support

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
   :role: validations_common/roles/advanced_format_512e_support
