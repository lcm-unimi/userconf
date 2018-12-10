#!/usr/bin/python
#
# Author: andreatsh - andreatsh@lcm.mi.infn.it

import ldap
import ldap.modlist as modlist
import pwd, sys, time

# Class to manage LDAP
class lcmldap():
    def __init__(self, uri, cn, dc, secret):
        self.conn   = None
        self.uri    = uri
        self.dc     = dc
        self.secret = secret
        try:
            self.conn = ldap.initialize(self.uri)
            self.conn.protocol_version = ldap.VERSION3
            self.conn.simple_bind_s(cn+","+self.dc,self.secret)
            print("Connection established.")
        except ldap.INVALID_CREDENTIALS:
            print("Your username or password is incorrect.")
            sys.exit()
        except ldap.LDAPError as e:
            if type(e.message) == dict and e.message.has_key('desc'):
                print(e.message['desc'])
            else: print(e)
            sys.exit()

    def __del__(self):
        self.conn.unbind_s()

    def adduser(self, name, surname, username, usersecret, expireDate, uidNo, badgenum):
        if (self.userexistsbyuid(username) ):
            print("User %s already exist!", username)
            return

        dn = "uid="+username+",ou=People,"+self.dc

        attrs = {}
        attrs['uid']            = username
        attrs['userPassword']   = usersecret
        attrs['givenName']      = name
        attrs['sn']             = surname
        attrs['cn']             = name+' '+surname
        attrs['objectClass']    = ['person',
                                   'organizationalPerson',
                                   'inetOrgPerson',
                                   'posixAccount',
                                   'top',
                                   'shadowAccount']
        attrs['shadowMax']      = '99999'
        attrs['shadowWarning']  = '7'
        attrs['shadowExpire']   = expireDate
        attrs['loginShell']     = '/bin/bash'
        attrs['uidNumber']      = uidNo
        attrs['gidNumber']      = '100'
        attrs['homeDirectory']  = '/home/'+username
        attrs['gecos']          = name+' '+surname+',,,,'+badgenum
        attrs['employeeNumber'] = badgenum
        attrs['mail']           = username+'@lcm.mi.infn.it'

        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = modlist.addModlist(attrs)

        # Do the actual synchronous add-operation to the ldapuri
        self.conn.add_s(dn,ldif)

    def userexistsbyuid(self, username):
        baseDN       = "ou=People,"+self.dc
        searchScope  = ldap.SCOPE_SUBTREE
        searchFilter = "uid="+username

        try:
            result = self.conn.search_s(baseDN, searchScope, searchFilter, None)
            if ( result==[] ):
                return False
            else:
                return True
        except ldap.LDAPError as e:
            print(e)
            return False

    def getusercredbyuid(self, username):
        baseDN         = "ou=People,"+self.dc
        searchScope    = ldap.SCOPE_SUBTREE
        searchFilter   = "uid="+username
        searchAttrList = ["givenName","sn"]

        try:
            # Result is a list of touple (one for each match) of dn and attrs.
            # Attrs is a dict, each value is a list of string.
            result = self.conn.search_s(baseDN, searchScope, searchFilter, searchAttrList)
            if ( result==[] ):
                print("User %s does not exist!", username)
                return
            result = [value[0] for value in result[0][1].values()]
            # Returns 2-element list, name and surname
            return result
        except ldap.LDAPError as e:
            print(e)
            return

    def changepwd(self, username, newsecret):
        if (not self.userexistsbyuid(username) ):
            print("User %s does not exist!", username)
            return

        dn = "uid="+username+",ou=People,"+self.dc
        try:
            self.conn.passwd( dn, None, newsecret )
        except ldap.LDAPError as e:
            print("Error: Can\'t change %s password: %s" % (username, e.message['desc']))

    def changeshadowexpire(self, username, shexp):
        if (not self.userexistsbyuid(username)):
            print("User %s does not exist!", username)
            return

        dn = "uid="+username+",ou=People,"+self.dc
        ldif = [( ldap.MOD_REPLACE, 'shadowExpire', shexp )]
        try:
            self.conn.modify_s(dn, ldif)
        except ldap.LDAPError as e:
            print("Error: Can\'t change %s shadowExpire: %s" % (username, e.message['desc']))

    def deluser(self, username):
        if (not self.userexistsbyuid(username) ):
            print("User %s does not exist!", username)
            return

        dn = "uid="+username+",ou=People,"+self.dc
        try:
            self.conn.delete_s(dn)
        except ldap.LDAPError as e:
            print("Error: Can\'t delete %s: %s" % (username, e.message['desc']))



def userexists(string):
    try:
        pwd.getpwnam(string).pw_name
        return True
    except KeyError:
        return False
