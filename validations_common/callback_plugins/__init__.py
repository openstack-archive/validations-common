"""
This module contains various callbacks developed to facilitate functions
of the Validation Framework.

Somewhat unorthodox naming of the callback classes is a direct result of how
ansible handles loading plugins.
The ansible determines the purpose of each plugin by looking at its class name.
As you can see in the 'https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/loader.py'
from the ansible repo, the loader uses the class names to categorize plugins.
This means that every callback plugin has to have the same class name,
and the unfortunate coder has to discern their purpose by checking
their module names.
"""
