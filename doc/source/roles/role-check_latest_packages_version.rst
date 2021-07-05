=============================
check_latest_packages_version
=============================

--------------
About The Role
--------------

An Ansible role to check if latest version of a list of packages is installed.

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
       packages_list:
         - coreutils
         - wget
     roles:
       - check_latest_packages_version

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
   :role: validations_common/roles/check_latest_packages_version
