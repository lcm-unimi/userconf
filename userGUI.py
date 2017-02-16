#!/usr/bin/python

# Author:       Gabriele Bozzola (sbozzolo)
# Email:        sbozzolator@gmail.com
# Date:         28.04.2016
# Last Edit:    16.02.2017 (andreatsh)

#~ This module is used to draw the interface
import npyscreen as nps
import checkpwd as cp
import lcmldap as ldap
from os import system as system
from re import search as search   
import pwd, time 

#~ This dictionary is intended to contain every string of Userconf,
#~ so it is easier to modify text and maintain the code compact

words = {
        'MainFormName'   : "Benvenuto in Userconf",
        'ExitText'       : "Esci",
        'MenuButtonText' : "Menu",
        'MainFormText'   : "Questo script ti permette di creare e modificare utenti sul cluster di LCM."
                           + " Per aprire il menu premi 'm' o seleziona MENU",
        'MainMenu'       : "Menu Principale",
        'AddUser'        : "Aggiungi Utente",
        'EditUser'       : "Modifica Utente",
        'EditPassword'   : "Modifica Password",
        'EditEmail'      : "Modifica Email",
        'EditBadgeNum'   : "Modifica Matricola",
        'DeleteUser'     : "Elimina Utente",
        'AboutUserconf'  : "Informazioni su Userconf",
        'ConfirmExit'    : "Sicuro di voler uscire?",
        'ExitUserconf'   : "Esci da Userconf",
        'Ldap'           : "DB password",
        'Name'           : "Nome",
        'Surname'        : "Cognome",
        'Username'       : "Nome Utente",
        'BadgeNum'       : "Matricola",
        'Email'          : "Email",
        'Password'       : "Password",
        'PasswordRepet'  : "Ripeti Password",
        'EmailConf'      : "Impostazione email",
        'Nothing'        : "Niente",
        'Forward'        : "Forward",
        'Rederict'       : "Rederict",
        'AppTitle'       : "LCM Userconf",
        'About'          : "About",
        'AboutApp'       : "Userconf versione 0.2.1",
        'ReturnToMain'   : "Torna al Menu",
        'NullPassword'   : "Inserisci una password!", 
        'WrongPassword'  : "Le due password inserite non coincidono",
        'BadPassword'    : "Password debole! Riprova!",
        'Add'            : "Crea",
        'Warning'        : "Attenzione!",
        'ConfirmUserExit': "Sicuro di voler uscire? Tutte le modifiche andranno perse!",
        'NoFeature'      : "Questa funzione non e' stata ancora implementata. Stay tuned!",
        'ConfirmDel'     : "Vuoi eliminare l'utente ",
        'AreYouSure'     : "Sei proprio sicuro di voler eliminare l'utente ",
        'ItCannotBeUndo' : "Una volta fatto non si puo' tornare indietro!",
        'RenewUser'      : "Rinnova Utente",
        'ExpDate1'       : "L'account dell'utente ",
        'ExpDate2'       : " scadra' il giorno ",
        'ExpDate3'       : " Rinnovare fino a ",
        'InsertUsername' : "Devi inserire l'username!",
        'BadChar'        : "Invalid character! ",
        'BadChar1'       : "Il carattere ",
        'BadChar2'       : " non e' ammesso!",
        'User'           : "L'utente ",
        'UserNotExist'   : " non esiste!",
        'UserExist'      : " esiste gia'! ",
        'NewUserCreated' : "User successfully created!"
}

class MainForm ( nps.ActionFormWithMenus ):
    """Class that draws the main screen of Userconf"""

    #~ Define a shortcut to open menu
    MENU_KEY = "m"

    #~ Rename button using Italian language
    OK_BUTTON_TEXT      = words['ExitText']
    CANCEL_BUTTON_TEXT  = words['MenuButtonText']

    #~ Create form elements and menus
    def create(self):
        """Add to the form the widgets"""
        #~ Text on main screen
        self.add(nps.TitleFixedText, name = words['MainFormName'], editable = False)
        self.add(nps.FixedText, value = words['MainFormText'], editable = False)

        #~ Main Menu and Edit User menu
        self.menu = self.new_menu(name = words['MainMenu'], shortcut = "m")
        self.menu.addItem(words['AddUser'], self.new_user, "n")
        self.edito = self.menu.addNewSubmenu( words['EditUser'], "d")
        self.edito.addItem(words['EditPassword'], self.edit_user, "p")
        self.edito.addItem(words['EditEmail'], self.edit_user, "e")
        self.edito.addItem(words['EditBadgeNum'], self.edit_user, "m")
        self.menu.addItem(words['RenewUser'], self.renew_user, "r")
        self.menu.addItem(words['DeleteUser'], self.delete_user, "c")
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
        """Launch EDITTEMPFORM form"""
        self.parentApp.setNextForm('EDITTEMPFORM')
        self.parentApp.switchFormNow()

    def delete_user(self):
        """Launch DELUSER form"""
        self.parentApp.setNextForm('DELUSER')
        self.parentApp.switchFormNow()


class NewUserForm (nps.ActionFormV2):
    """Class that handles the creation of a user"""

    #~ Rename button using Italian language
    OK_BUTTON_TEXT      = words['Add']
    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        """Add to the form the widgets"""
        self.ldap     = self.add(nps.TitlePassword, name = words['Ldap'], begin_entry_at = 25)
        self.nname    = self.add(nps.TitleText, name = words['Name'], begin_entry_at = 25)
        self.surname  = self.add(nps.TitleText, name = words['Surname'], begin_entry_at = 25)
        self.username = self.add(nps.TitleText, name = words['Username'], begin_entry_at = 25)
        self.userpass = self.add(nps.TitlePassword, name = words['Password'], begin_entry_at = 25)
        self.passrepe = self.add(nps.TitlePassword, name = words['PasswordRepet'], begin_entry_at = 25)
        self.badgenum = self.add(nps.TitleText, name = words['BadgeNum'], begin_entry_at = 25)
        self.email    = self.add(nps.TitleText, name = words['Email'], begin_entry_at = 25)
#        self.emailcon = self.add(nps.TitleSelectOne, name = words['EmailConf'], begin_entry_at = 25,
#                   values = [words['Forward'],words['Rederict'],words['Nothing']], scroll_exit = True)

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
            return 
        if (self.userpass.value != self.passrepe.value):
            nps.notify_confirm(words['WrongPassword'], words['Warning'])
            return 
        if (cp.ispwdweak(self.userpass.value)): 
            nps.notify_confirm(words['BadPassword'], words['Warning'])
            return 

        # Check empty fields
        # TODO: add specific error messages 
        if (self.ldap.value == ""):
            nps.notify_confirm(words['Warning'], words['Warning'])
            return 
        if (self.nname.value == ""):
            nps.notify_confim(words['Warning'], words['Warning'])
            return
        if (self.surname.value == ""):
            nps.notify_confim(words['Warning'], words['Warning'])
            return
        if (self.username.value == ""):
            nps.notify_confim(words['Warning'], words['InsertUsername'])
            return
        if (self.badgenum.value == ""):
            nps.notify_confim(words['Warning'], words['Warning'])
            return
        if (self.email.value == ""):
            nps.notify_confirm(words['Warning'], words['Warning'])
            return
#        if (self.emailcon.value == ""):
#            nps.notify_confirm(words['Warning'], words['Warning'])
#            return 

        # Check if fields contains bad chars
        if (search(r'[^A-Za-z0-9_]', self.nname.value)    or
            search(r'[^A-Za-z0-9_]', self.surname.value)  or
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
            db = ldap.lcmldap("ldaps://xx8.xx1.xx.xxxx.it/", 
                              "cn=Manager,dc=xx8,dc=xx1", self.ldap.value)
        except:
            nps.notify_confirm(words['Warning'], words['Warning'])
            return 

        # Add user on main server
        templist = []
        for i in pwd.getpwall():
            if (i.pw_uid<64000): templist.append(i.pw_uid)
        useruidNo=str( max(templist)+1 )
        expDate=str( (int(time.time())+3*86400*365) / 86400 )
        addusercmd="useradd -u "+useruidNo+                            \
                   " -c "+self.nname.value+",,,,"+self.badgenum.value+ \
                   " -d /home/"+self.username.value+                   \
                   " -g users -m -s /bin/bash"+                        \
                   " -e "+expDate+" "+self.username.value
       
        system(addusercmd)

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
#        self.emailcon.value = None
        self.editing        = False
        self.parentApp.setNextForm("MAIN")
        self.parentApp.switchFormNow()


class EditTempForm (nps.ActionFormV2):
    """Class that asks the username which has to be edited"""

    #~ Rename button using Italian language
    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        self.show_atx = 66
        self.show_aty = 20
        self.uname = self.add(nps.TitleText, name = words['Username'])

    def on_cancel(self):
        """Discard edits and return to the main screen"""
        self.uname.value = ""
        self.return_to_main_screen()

    def on_ok(self):
        pass

    def return_to_main_screen(self):
        """Return to the main screen"""
        self.parentApp.setNextForm("MAIN")
        self.editing = False
        self.parentApp.switchFormNow()


class DelForm (nps.ActionFormV2):
    """Class that deletes an user"""

    #~ Rename button using Italian language
    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        self.show_atx = 66
        self.show_aty = 20
        self.uname = self.add(nps.TitleText, name = words['Username'])

    def on_cancel(self):
        """Discard edits and return to the main screen"""
        self.uname.value = ""
        self.return_to_main_screen()

    def on_ok(self):
        #~ Check if user exist
        dele = nps.notify_yes_no(words['ConfirmDel']+self.uname.value+"?",
                                 words['DeleteUser'], editw = 2)
        if (dele):
            dele2 = nps.notify_yes_no(words['AreYouSure']+self.uname.value+"?\n"+ 
                    words['ItCannotBeUndo'], words['DeleteUser'], editw = 2)

    def return_to_main_screen(self):
        """Return to the main screen"""
        self.parentApp.setNextForm("MAIN")
        self.editing = False
        self.parentApp.switchFormNow()


class RenewForm (nps.ActionFormV2):
    """Class that rennews an user"""

    #~ Rename button using Italian language
    CANCEL_BUTTON_TEXT  = words['ReturnToMain']

    def create(self):
        self.show_atx = 66
        self.show_aty = 20
        self.uname = self.add(nps.TitleText, name = words['Username'])

    def on_cancel(self):
        """Discard edits and return to the main screen"""
        self.uname.value = ""
        self.return_to_main_screen()

    def on_ok(self):
        #~ Check if user exist
        if (self.uname.value == ""):
            nps.notify_confirm(words['InsertUsername'], words['Warning'])
        else:
            pass

    def return_to_main_screen(self):
        """Return to the main screen"""
        self.parentApp.setNextForm("MAIN")
        self.editing = False
        self.parentApp.switchFormNow()


class GUI (nps.NPSAppManaged):
    """Defines the whole application GUI"""

    def onStart(self):
        """Adds the forms"""
        self.addForm('MAIN', MainForm, name = words['AppTitle']) 
        self.addForm('NEWUSER', NewUserForm, name = words['AddUser'])
        self.addForm('EDITTEMPFORM', EditTempForm, name = words['EditUser'], lines = 6, columns = 45)
        self.addForm('DELUSER', DelForm, name = words['DeleteUser'], lines = 6, columns = 45)
        self.addForm('RENEWUSER', RenewForm, name = words['RenewUser'], lines = 6, columns = 45)

