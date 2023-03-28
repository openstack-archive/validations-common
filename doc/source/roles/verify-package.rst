================
verify-package
================

--------------
About The Role
--------------

An Ansible role which runs `rpm --verify` on RedHat OS family and
returns the status.

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
       - verify-package

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
   :role: validations_common/roles/verify-package
