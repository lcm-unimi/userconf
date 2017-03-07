#!/usr/bin/python

# Author:       Gabriele Bozzola (sbozzolo)
# Email:        sbozzolator@gmail.com
# Date:         28.04.2016
# Last Edit:    06.03.2017 (andreatsh)

#~ This module is used to draw the interface
import npyscreen as nps
import checkpwd as cp
import lcmldap as ldap
from os import system as system
from re import search as search
import pwd, smtplib, time

#~ This dictionary is intended to contain every string of Userconf,
#~ so it is easier to modify text and maintain the code compact

words = {
    'MainFormName'   : "Welcome to Umanager",
    'ExitText'       : "Quit",
    'MenuButtonText' : "Menu",
    'MainFormText1'  : "This script allows you to perform "
                       +"actions on LCM users database. ",
    'MainFormText2'  : "To open the menu press 'm' or select MENU",
    'MainMenu'       : "Main Menu",
    'AddUser'        : "Add User",
    'EditPassword'   : "Edit Password",
    'DeleteUser'     : "Delete User",
    'AboutUserconf'  : "About Userconf",
    'ConfirmExit'    : "Do you reallly want to quit?",
    'ExitUserconf'   : "Quit Userconf",
    'Ldap'           : "Ldap password",
    'Name'           : "First name",
    'Surname'        : "Last name",
    'Username'       : "Username",
    'BadgeNum'       : "Badge number",
    'Email'          : "Email",
    'Password'       : "Enter Password",
    'PasswordRepet'  : "Retype Password",
    'AppTitle'       : "LCM Userconf",
    'About'          : "About",
    'AboutApp'       : "Userconf version 1.0.0",
    'ReturnToMain'   : "BackToMenu",
    'LdapPassword'   : "Enter LDAP password!",
    'NullPassword'   : "Enter a valid password!",
    'WrongPassword'  : "Passwords do not match!",
    'BadPassword0'   : "Short password! Try again!",
    'BadPassword1'   : "Password can not contain spaces or tabs! Try again!",
    'BadPassword2'   : "Password based on user credentials!",
    'BadPassword3'   : "Password should contain at least three chars type!",
    'Add'            : "Done",
    'Warning'        : "Warning!",
    'ConfirmUserExit': "Do you really want to quit? All changes will be lost!",
    'ConfirmDel'     : "Do you want to delete user? ",
    'AreYouSure'     : "Do you really want to delete this user?",
    'ItCannotBeUndo' : "This action can not be undone!",
    'RenewUser'      : "Renew User",
    'ExpDate1'       : "User account ",
    'ExpDate2'       : " will expire on the day ",
    'ExpDate3'       : " Renew until ",
    'InsertUsername' : "Insert a valid username!",
    'InsertName'     : "Insert user's first name!",
    'InsertSurname'  : "Insert user's last name!",
    'InsertBadgeNo'  : "Insert user's badge number!",
    'InsertEmail'    : "Insert user's email for redirection!",
    'BadChar'        : "Invalid character! ",
    'DBConnFail'     : "Failed connection with LDAP! Retype LDAP password!",
    'User'           : "The user ",
    'UserNotExist'   : " does not exist!",
    'UserExist'      : " already exists! ",
    'RenewUser1'     : "Do you want to renew ",
    'RenewUser2'     : "'s account until the day: ",
    'MailSent'       : "Successfully sent mail!",
    'MailNotSent'    : "Unable to sent mail!",
    'NewUserCreated' : "User successfully created!",
    'UserDeleted'    : "User successfully deleted!",
    'PasswordEdited' : "User's password successfully changed!",
    'UserRenewed'    : "User's account successfully renewed!"

}

class MainForm ( nps.ActionFormWithMenus ):
    """Class that draws the main screen of Userconf"""

    #~ Define a shortcut to open menu
    MENU_KEY = "m"

    OK_BUTTON_TEXT      = words['ExitText']
    CANCEL_BUTTON_TEXT  = words['MenuButtonText']

    #~ Create form elements and menus
    def create(self):
        """Add to the form the widgets"""
        #~ Text on main screen
        self.add(nps.TitleFixedText, name = words['MainFormName'], editable = False)
        self.add(nps.FixedText, value = words['MainFormText1'], editable = False)
        self.add(nps.FixedText, value = words['MainFormText2'], editable = False)

        #~ Main Menu and Edit User menu
        self.menu = self.new_menu(name = words['MainMenu'], shortcut = "m")
        self.menu.addItem(words['AddUser'], self.new_user, "n")
        self.menu.addItem(words['EditPassword'], self.edit_user, "p")
        self.menu.addItem(words['RenewUser'], self.renew_user, "r")
        self.menu.addItem(words['DeleteUser'], self.delete_user, "d")
        self.menu.addItem(words['AboutUserconf'], self.about, "a")
        self.menu.addItem(words['ExitUserconf'], self.exit_application, "e")

    def on_cancel(self):
        """Displays the main menu when the button cancel is pressed"""
        self.popup_menu(self.menu)

    def on_ok(self):
        """Ask a confirmation for exiting"""
        exiting = nps.notify_yes_no(words['ConfirmExit'], words['ExitText'], editw = 2)
        if (exiting):
            self.exit_application()
        else:
            pass #~ Do nothing

    def about(self):
        """Displys info about the Userconf script"""
        nps.notify_confirm(words['AboutApp'], words['About'], editw=1)

    def exit_application(self):
        """Closes the GUI"""
        self.editing = False
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def renew_user(self):
        """Launch RENEW form"""
        self.parentApp.setNextForm('RENEWUSER')
        self.parentApp.switchFormNow()

    def new_user(self):
        """Launch NEWUSER form"""
        self.parentApp.setNextForm('NEWUSER')
        self.parentApp.switchFormNow()

    def edit_user(self):
        """Launch EDITUSERPWDFORM form"""
        self.parentApp.setNextForm('EDITUSERPWDFORM')
        self.parentApp.switchFormNow()

    def delete_user(self):
        """Launch DELUSER form"""
        self.parentApp.setNextForm('DELUSER')
        self.parentApp.switchFormNow()


class NewUserForm (nps.ActionFormV2):
    """Class that handles the creation of a user"""

    OK_BUTTON_TEXT      = words['Add']
    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        """Add to the form the widgets"""
        self.ldap     = self.add(nps.TitlePassword, name = words['Ldap'], begin_entry_at = 20)
        self.nname    = self.add(nps.TitleText, name = words['Name'], begin_entry_at = 20)
        self.surname  = self.add(nps.TitleText, name = words['Surname'], begin_entry_at = 20)
        self.username = self.add(nps.TitleText, name = words['Username'], begin_entry_at = 20)
        self.userpass = self.add(nps.TitlePassword, name = words['Password'], begin_entry_at = 20)
        self.passrepe = self.add(nps.TitlePassword, name = words['PasswordRepet'], begin_entry_at = 20)
        self.badgenum = self.add(nps.TitleText, name = words['BadgeNum'], begin_entry_at = 20)
        self.email    = self.add(nps.TitleText, name = words['Email'], begin_entry_at = 20)

    def on_cancel(self):
        """Return to the main screen when the button cancel is pressed"""
        exiting = nps.notify_yes_no(words['ConfirmUserExit'], words['ExitText'], editw = 2)
        if (exiting):
            self.return_to_main_screen()
        else:
            pass #~ Do nothing

    def on_ok(self):

        """Checks and create the user"""
        # First of all, check password
        # In my experience this is the most difficult step --andreatsh
        if (self.userpass.value=="" or self.passrepe.value==""):
            nps.notify_confirm(words['NullPassword'], words['Warning'])
            self.userpass.value = None
            self.passrepe.value = None
            return
        if (self.userpass.value != self.passrepe.value):
            nps.notify_confirm(words['WrongPassword'], words['Warning'])
            self.userpass.value = None
            self.passrepe.value = None
            return

        tp = cp.ispwdweak(self.userpass.value,self.nname.value,
                          self.surname.value,self.username.value)
        if (tp[0]):
            if (tp[1]==0):
                nps.notify_confirm(words['BadPassword0'], words['Warning'])
            elif (tp[1]==1):
                nps.notify_confirm(words['BadPassword1'], words['Warning'])
            elif (tp[1]==2):
                nps.notify_confirm(words['BadPassword2'], words['Warning'])
            elif (tp[1]==3):
                nps.notify_confirm(words['BadPassword3'], words['Warning'])
            self.userpass.value = None
            self.passrepe.value = None
            return

        # Check empty fields
        if (self.ldap.value == ""):
            nps.notify_confirm(words['LdapPassword'], words['Warning'])
            return
        if (self.nname.value == ""):
            nps.notify_confim(words['InsertName'], words['Warning'])
            return
        if (self.surname.value == "InsertSurname"):
            nps.notify_confim(words['Warning'], words['Warning'])
            return
        if (self.username.value == ""):
            nps.notify_confim(words['InsertUsername'], words['InsertUsername'])
            return
        if (self.badgenum.value == ""):
            nps.notify_confim(words['InsertBadgeNo'], words['Warning'])
            return
        if (self.email.value == ""):
            nps.notify_confirm(words['InsertEmail'], words['Warning'])
            return

        # Check if fields contains bad chars
        if (search(r'[^A-Za-z0-9_\s]', self.nname.value)    or
            search(r'[^A-Za-z0-9_\s]', self.surname.value)  or
            search(r'[^A-Za-z0-9_]', self.username.value) or
            search(r'[^A-Za-z0-9_]', self.badgenum.value)):
            nps.notify_confirm(words['BadChar'], words['Warning'], editw = 1)
            return

        # Check if the chosen username already exists
        if(ldap.userexists(self.username.value)):
            errormsg = words['User']+self.username.value+words['UserExist']
            nps.notify_confirm(errormsg, words['Warning'], editw = 1)
            return
        # else no user with chosen username exists: do nothing

        try:
            db = ldap.lcmldap("ldaps://xx8.xx1.mi.infn.it/",
                              "cn=Manager","dc=xx8,dc=xx1", self.ldap.value)
        except:
            nps.notify_confirm(words['DBConnFail'], words['Warning'])
            self.ldap.value = None
            return

        # Add user on main server
        templist = []
        for i in pwd.getpwall():
            if (i.pw_uid<64000): templist.append(i.pw_uid)
        useruidNo=str( max(templist)+1 )
        expDate=str( (int(time.time())+3*86400*365) / 86400 )
        addusercmd='useradd -u '+useruidNo+                                 \
                   ' -c "'+self.nname.value+',,,,'+self.badgenum.value+'"'+ \
                   ' -d /home/'+self.username.value+                        \
                   ' -g users -m -s /bin/bash'+                             \
                   ' -e '+expDate+' '+self.username.value

        try: 
            system(addusercmd)
        except:
            nps.notify_confirm(words['Warning'], words['Warneng'])
            return

        # Add user to LDAP database
        db.adduser(self.nname.value,self.surname.value,self.username.value,
                   self.userpass.value,expDate,useruidNo,self.badgenum.value)
        

        # Configure user's mail
        mforwardfile="/home/"+self.username.value+"/.forward"
        ofs = open(mforwardfile,"w")
        ofs.write(self.username.value)
        ofs.write("\n")
        ofs.write(self.email.value)
        ofs.close()

        # Limit user's disk quota
        quotacmd="edquota -p lcm-quota -f /home "+self.username.value
        system(quotacmd)

        nps.notify_confirm(words['NewUserCreated'], words['Warning'])

        self.return_to_main_screen()

    def return_to_main_screen(self):
        """Clear values and return to the main screen"""
        self.ldap.value     = None
        self.nname.value    = None
        self.surname.value  = None
        self.username.value = None
        self.userpass.value = None
        self.passrepe.value = None
        self.badgenum.value = None
        self.email.value    = None
        self.editing        = False
        self.parentApp.setNextForm("MAIN")
        self.parentApp.switchFormNow()


class EditUserPwdForm (nps.ActionFormV2):
    """Class that asks the username which has to be edited"""

    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        self.show_atx = 66
        self.show_aty = 20
        self.ldap     = self.add(nps.TitlePassword, name = words['Ldap'], begin_entry_at = 20)
        self.nname    = self.add(nps.TitleText, name = words['Name'], begin_entry_at = 20)
        self.surname  = self.add(nps.TitleText, name = words['Surname'], begin_entry_at = 20)
        self.username = self.add(nps.TitleText, name = words['Username'], begin_entry_at = 20)
        self.userpass = self.add(nps.TitlePassword, name = words['Password'], begin_entry_at = 20)
        self.passrepe = self.add(nps.TitlePassword, name = words['PasswordRepet'], begin_entry_at = 20)

    def on_cancel(self):
        """Discard edits and return to the main screen"""
        self.return_to_main_screen()

    def on_ok(self):
        # Check fields validity
        if (self.ldap.value == ""):
            nps.notify_confirm(words['LdapPassword'], words['Warning'])
            return
        if (self.nname.value == ""):
            nps.notify_confim(words['InsertName'], words['Warning'])
            return
        if (self.surname.value == ""):
            nps.notify_confim(words['InsertSurname'], words['Warning'])
            return
        if (self.username.value == ""):
            nps.notify_confim(words['InsertUsername'], words['Warning'])
            return
        # Check if fields contains bad chars
        if (search(r'[^A-Za-z0-9_]', self.nname.value)    or
            search(r'[^A-Za-z0-9_]', self.surname.value)  or
            search(r'[^A-Za-z0-9_]', self.username.value)):
            nps.notify_confirm(words['BadChar'], words['Warning'])
            return

        # Check password
        if (self.userpass.value=="" or self.passrepe.value==""):
            nps.notify_confirm(words['NullPassword'], words['Warning'])
            self.userpass.value = None
            self.passrepe.value = None
            return
        if (self.userpass.value != self.passrepe.value):
            nps.notify_confirm(words['WrongPassword'], words['Warning'])
            self.userpass.value = None
            self.passrepe.value = None
            return

        tp = cp.ispwdweak(self.userpass.value,self.nname.value,
                          self.surname.value,self.username.value)
        if (tp[0]):
            if (tp[1]==0):
                nps.notify_confirm(words['BadPassword0'], words['Warning'])
            elif (tp[1]==1):
                nps.notify_confirm(words['BadPassword1'], words['Warning'])
            elif (tp[1]==2):
                nps.notify_confirm(words['BadPassword2'], words['Warning'])
            elif (tp[1]==3):
                nps.notify_confirm(words['BadPassword3'], words['Warning'])
            self.userpass.value = None
            self.passrepe.value = None
            return

        # Check if this user exists
        if(ldap.userexists(self.username.value)):
            pass
        else:
            errormsg = words['User']+self.username.value+words['UserExist']
            nps.notify_confirm(errormsg, words['Warning'], editw = 1)
            return

        # Try to connect to LDAP database
        try:
            db = ldap.lcmldap("ldaps://xx8.xx1.mi.infn.it/",
                              "cn=Manager","dc=xx8,dc=xx1", self.ldap.value)
        except:
            nps.notify_confirm(words['DBConnFail'], words['Warning'])
            self.ldap.value = None
            return

        db.changepwd(self.username.value,self.userpass.value)

        nps.notify_confirm(words['PasswordEdited'], words['Warning'])

        self.return_to_main_screen()

    def return_to_main_screen(self):
        """Return to the main screen"""
        self.ldap.value  = None
        self.nname.value = None
        self.surname.value = None
        self.username.value = None
        self.userpass.value = None
        self.passrepe.value = None
        self.editing = False
        self.parentApp.setNextForm("MAIN")
        self.parentApp.switchFormNow()


class DelUserForm (nps.ActionFormV2):
    """Class that deletes an user"""

    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        self.show_atx = 66
        self.show_aty = 20
        self.ldap  = self.add(nps.TitlePassword, name = words['Ldap'], begin_entry_at = 20)
        self.uname = self.add(nps.TitleText, name = words['Username'], begin_entry_at = 20)

    def on_cancel(self):
        """Discard edits and return to the main screen"""
        self.return_to_main_screen()

    def on_ok(self):
        # Check fields validity
        if (self.ldap.value == ""):
            nps.notify_confirm(words['LdapPassword'], words['Warning'])
            return
        if (self.uname.value == ""):
            nps.notify_confim(words['InsertUsername'], words['Warning'])
            return

        # Check if this user exists
        if(ldap.userexists(self.uname.value)):
            pass
        else:
            errormsg = words['User']+self.uname.value+words['UserNotExist']
            nps.notify_confirm(errormsg, words['Warning'], editw = 1)
            return

        # Try to connect to LDAP database
        try:
            db = ldap.lcmldap("ldaps://xx8.xx1.mi.infn.it/",
                              "cn=Manager","dc=xx8,dc=xx1", self.ldap.value)
        except:
            nps.notify_confirm(words['DBConnFail'], words['Warning'])
            self.ldap.value = None
            return

        # Ask to confirm you really want to delete this user
        dele = nps.notify_yes_no(words['ConfirmDel']+self.uname.value+"?",
                                 words['DeleteUser'], editw = 2)
        if (dele):
            dele2 = nps.notify_yes_no(words['AreYouSure']+self.uname.value+"?\n"+
            words['ItCannotBeUndo'], words['DeleteUser'], editw = 2)
            if (dele2):
                pass
            else:
                return
        else:
            return

        delusercmd="userdel -r "+self.uname.value
        system(delusercmd)

        db.deluser(self.uname.value)

        nps.notify_confirm(words['UserDeleted'], words['Warning'])

        self.return_to_main_screen()


    def return_to_main_screen(self):
        """Return to the main screen"""
        self.ldap.value  = None
        self.uname.value = None
        self.editing = False
        self.parentApp.setNextForm("MAIN")
        self.parentApp.switchFormNow()


class RenewForm (nps.ActionFormV2):
    """Class that rennews an user"""

    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        self.show_atx = 66
        self.show_aty = 20
        self.ldap  = self.add(nps.TitlePassword, name = words['Ldap'], begin_entry_at = 20)
        self.uname = self.add(nps.TitleText, name = words['Username'], begin_entry_at = 20)

    def on_cancel(self):
        """Discard edits and return to the main screen"""
        self.return_to_main_screen()

    def on_ok(self):
        # Check fields validity
        if (self.ldap.value == ""):
            nps.notify_confirm(words['LdapPassword'], words['Warning'])
            return
        if (self.uname.value == ""):
            nps.notify_confirm(words['InsertUsername'], words['Warning'])
            return
        if (search(r'[^A-Za-z0-9_]', self.uname.value)):
            nps.notify_confirm(words['BadChar'], words['Warning'])
            return

        # Check if this user exists
        if(ldap.userexists(self.uname.value)):
            pass
        else:
            errormsg = words['User']+self.uname.value+words['UserNotExist']
            nps.notify_confirm(errormsg, words['Warning'], editw = 1)
            return

        # Try to connect to LDAP database
        try:
            db = ldap.lcmldap("ldaps://xx8.xx1.mi.infn.it/",
                              "cn=Manager","dc=xx8,dc=xx1", self.ldap.value)
        except:
            nps.notify_confirm(words['DBConnFail'], words['Warning'])
            self.ldap.value = None
            return

        newday = time.gmtime(time.time()+3*86400*365)
        newdaystr = time.strftime("%d/%m/%Y", newday)
        # Convert in the right format for chage command
        newshadow = time.strftime("%m/%d/%Y", newday)

        text = words['RenewUser1'] + self.uname.value + words['RenewUser2'] 
        text = text + newdaystr + "?" 

        ren = nps.notify_yes_no(text, words['RenewUser'], editw = 2)
        if (not ren):
            self.return_to_main_screen()
            return
 
        cmd = "chage " + self.uname.value + " -E " + newshadow
        expDate=str( (int(time.time())+3*86400*365) / 86400 )
    
        db.changeshadowexpire(self.uname.value, expDate)
        system(cmd) 

       
        # Send mail to user 
        sender    = 'staff@lcm.mi.infn.it'
        usermail  = self.uname.value + "@lcm.mi.infn.it"
        receivers = [ usermail, 'working@lcm.mi.infn.it' ]

        message = """From: <staff@lcm.mi.infn.it>
To: """ + usermail + """
Subject: Rinnovo account LCM
Reply-to: <working@lcm.mi.infn.it>

Ciao, 

abbiamo rinnovato il tuo account.
Nuova data di scadenza: """ + newdaystr + """

A presto,
LCM Staff
"""

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)         
            nps.notify_confirm(words['MailSent'], words['Warning'])
        except smtplib.SMTPException:
            nps.notify_confirm(words['MailNotSent'], words['Warning'])

        nps.notify_confirm(words['UserRenewed'], words['Warning'])
        self.return_to_main_screen()


    def return_to_main_screen(self):
        """Return to the main screen"""
        self.ldap.value  = None
        self.uname.value = None
        self.parentApp.setNextForm("MAIN")
        self.editing = False
        self.parentApp.switchFormNow()


class GUI (nps.NPSAppManaged):
    """Defines the whole application GUI"""

    def onStart(self):
        """Adds the forms"""
        self.addForm('MAIN', MainForm, name = words['AppTitle'])
        self.addForm('NEWUSER', NewUserForm, name = words['AddUser'])
        self.addForm('EDITUSERPWDFORM', EditUserPwdForm, name = words['EditPassword'], lines = 10, columns = 70)
        self.addForm('DELUSER', DelUserForm, name = words['DeleteUser'], lines = 10, columns = 70)
        self.addForm('RENEWUSER', RenewForm, name = words['RenewUser'], lines = 10, columns = 70)
