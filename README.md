# pyinfra-ansible-inventory-connector

pyinfra-ansible-inventory-connector lets you use your Ansible inventories with pyinfra 3.x.

Instead of building a parser for Ansible inventories as was tried in pyinfra pre 3.x, this connector just uses the Ansible Python API to do the heavy lifting.

## Build and install

```bash
pip install .
```

## Usage

```bash
pyinfra @ansible/path/to/inventory deploy.py # relative path
pyinfra @ansible//path/to/inventory deploy.py # absolute path
```
