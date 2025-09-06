from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

from pyinfra.connectors.base import BaseConnector

keys_to_remove = [
    "group_names",
    "failed",
    "groups",
    "inventory_file",
    "inventory_hostname",
    "playbook_dir",
    "omit",
    "ansible_config_file",
    "inventory_hostname_short",
    "ansible_python_interpreter",
    "ansible_playbook_python",
    "ansible_facts",
    "ansible_version",
    "inventory_dir"
]

keys_to_rename = {
    "ansible_become": "_sudo",
    "ansible_port": "ssh_port",
    "ansible_host": "ssh_hostname",
    "ansible_user": "ssh_user"
}


def translate_vars(host_vars):
    for key in keys_to_remove:
        host_vars.pop(key, None)

    for old_key, new_key in keys_to_rename.items():
        if old_key in host_vars:
            host_vars[new_key] = host_vars.pop(old_key)

    return host_vars


class AnsibleInventoryConnector(BaseConnector):
    """

    A connector that uses Ansible Python API to expose ansible inventories to pyinfra.
    Usage:  pyinfra @ansible/path/to/inventory deploy.py (relative path)
            pyinfra @ansible//path/to/inventory deploy.py (absolute path)

    """
    handles_execution = False

    @staticmethod
    def make_names_data(inventory_string = None):
        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=inventory_string)
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        for host in inventory.get_hosts():
            host_vars = variable_manager.get_vars(host=host)
            groups = host_vars['group_names']
            vars = translate_vars(host_vars)
            yield host.name, vars, groups
