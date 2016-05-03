#!/usr/bin/python


import ldap
import ldap.modlist as modlist
import getpass, pwd, sys, time 

class lcmldap():
    def __init__(self, uri, bind, secret):
        self.conn = None
        self.uri = uri
        self.bind = bind 
        self.secret = secret
        try:
            self.conn = ldap.initialize(self.uri)
            self.conn.protocol_version = ldap.VERSION3
            self.conn.simple_bind_s(self.bind,self.secret)
            print 'Connection established.'
        except ldap.LDAPError as e:
            if type(e.message) == dict and e.message.has_key('desc'):
                print e.message['desc']
            else:
                print e

    def __del__(self):
        self.conn.unbind_s()

    def add_user(self, name, surname, username, usersecret, badgenum):
        dn = "uid="+username+",ou=People,dc=nanos8,dc=pcteor1" 

        attrs = {}

        attrs['uid'] =  username
        attrs['userPassword'] = usersecret
        # FIXME: 
        # La password puo' esser passata o in chiaro oppure nel seguente formato:
        # userPassword: {CRYPT}xxxxxxxxxx
        # Tuttavia ldap non fara` piu' alcun controllo sulla robustezza della password
        # Per cui il controllo sarebbe da fare prima di passare il valore alla funzione
        attrs['givenName'] = name
        attrs['sn'] =  surname
        attrs['cn'] = name+' '+surname 
        attrs['objectClass'] = ['person', 'organizationalPerson', 'inetOrgPerson', 
                                'posixAccount', 'top', 'shadowAccount']
        attrs['shadowMax'] = '99999'
        attrs['shadowWarning'] = '7'
        attrs['shadowExpire'] = str( (int(time.time())+3*86400*365) / 86400 )
        attrs['loginShell'] = '/bin/bash'
        # WARNING: l'utente deve prima esser creato ed esistere su nanos8 
        attrs['uidNumber'] = str(pwd.getpwnam(username).pw_uid)
        attrs['gidNumber'] = '100'
        attrs['homeDirectory'] = '/home/'+username
        attrs['gecos'] =  name+' '+surname+',,,,'+badgenum
        attrs['employeeNumber'] = badgenum
        attrs['mail'] = username+'@lcm.mi.infn.it'        

        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = modlist.addModlist(attrs)

        # Do the actual synchronous add-operation to the ldapuri
        self.conn.add_s(dn,ldif)

    def del_user(self, username):
        dn = "uid="+username+",ou=People,dc=nanos8,dc=pcteor1"
        try:
            self.conn.delete_s(dn)
        except ldap.LDAPError as e:
            print 'Error: Can\'t delete %s: %s' % (username, e.message['desc'])


# FIXME: aggiungere un controllo in modo che db venga istanziato correttamente && db.conn != None
db = lcmldap("ldaps://localhost.localdomain/", "cn=Manager,dc=n8,dc=pct1",  
             getpass.getpass("Insert LDAP password: " ))



