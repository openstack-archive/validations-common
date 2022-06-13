Role Name
=========

Call `rpm --verify <package>'. Note that this validation only works for
rhel-based systems, such as Enterprise Linux, CentOS, Fedora and so on.

Requirements
------------

None

Role Variables
--------------

`verify_package_pkg`: (str) Package name to verify
`verify_package_verbose`: (bool) toggle verbose option for rpm

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      vars:
        verify_package_pkg: openstack-selinux
      roles:
         - verify_package

License
-------

BSD
