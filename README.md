# umanager
umanager is a python script to manage users accounts.

umanager is designed to:
* create users accounts on our main server and add it to a LDAP database
* delete users accounts from main server and LDAP database
* change users password in LDAP database
* renew users shadow expire date

umanager.py import:
* userGUI.py to manage the graphical user interface
* lcmldap.py to manage connections with LDAP database

## Prerequisites
Requires npyscreen >= 4.4.0
Requires superuser privileges.

