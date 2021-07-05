================
validate_selinux
================

--------------
About The Role
--------------

An Ansible role to ensure we don't have any SELinux denials on the host(s).

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
       validate_selinux_working_dir: /tmp
       validate_selinux_audit_source: /var/log/audit/audit.log
       validate_selinux_skip_list_dest: "{{ validate_selinux_working_dir }}/denials-skip-list.txt"
       validate_selinux_filtered_denials_dest: "{{ validate_selinux_working_dir }}/denials-filtered.log"
       validate_selinux_strict: false
       validate_selinux_filter: "None"
       validate_selinux_skip_list:
         - entry: 'tcontext=system_u:system_r:init_t'
           comment: 'This one is a real-life entry'
         - entry: 'tcontext=system_u:system_r:system_dbusd_t'
           comment: 'This one is another real-life entry'
     roles:
       - validate_selinux

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
   :role: validations_common/roles/validate_selinux
