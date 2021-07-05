===============
xfs_check_ftype
===============

--------------
About The Role
--------------

An Ansible role to check if there is at least 1 XFS volume with ftype=0 in any
deployed server(s).

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
       - xfs_check_ftype

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
   :role: validations_common/roles/xfs_check_ftype
