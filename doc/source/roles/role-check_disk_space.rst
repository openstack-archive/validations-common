================
check_disk_space
================

--------------
About The Role
--------------

An Ansible role to check that the partitioning schema on the host(s) has enough
free space.

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
       volumes:
         - { mount: /home, min_size: 25 }
         - { mount: /, min_size: 50 }
     roles:
       - check_disk_space

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
   :role: validations_common/roles/check_disk_space
