==================
check_selinux_mode
==================

--------------
About The Role
--------------

An Ansible role to check SELinux status on the host(s).

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
       - check_selinux_mode

License
=======

Apache

Author Information
==================

**Red Hat TripleO DFG:Security**

----------------
Full Description
----------------

.. ansibleautoplugin::
   :role: validations_common/roles/check_selinux_mode
