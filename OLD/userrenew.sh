#!/bin/bash
#userrenew.sh - add +3 years to user's shadowExpire
# by jp (2013)
MANAGER="cn=Manager"
BIND="dc=xxx.xxx,dc=yyy.yyy"
TMPFILE="/tmp/umod.ldif"
#TMPFILE=tempfile.tmp

#FROM HERE...
clean(){
    stty echo
    rm $TMPFILE
    exit $1;
}

help(){
        echo "Usage: $0 <Username>"
        exit -1;
}

[ -z $1 ] && help

trap "clean -2" SIGINT SIGTERM

ldapsearch -x -A "uid=$1" > $TMPFILE

NENT=$(grep numEntries $TMPFILE | cut -d ':' -f 2)
 
[ -z $NENT ] || [ $NENT -ne 1 ] && \
echo User not found && clean -1;

# TO HERE, COPY-PASTED FROM USERMOD.SH; input checks and cleanup routine.

NEWYEAR="20`date +%y`"
NEWYEAR=$(($NEWYEAR+3))
MONTH=`date +%m`
DAY=`date +%d`

NEWSHADOW=$((`date --date="$NEWYEAR-$MONTH-$DAY" +%s`/ 86400)) #add +3 years to the shadowExpire

echo
echo La data di scadenza dell\'utente $1 verra\' modificata come segue:

DN=$(ldapsearch -x "uid=$1" shadowExpire \
	| grep dn: | cut -f2 -d':')
echo
{
	echo "dn: $DN"
	echo "changetype: modify"
	echo "replace: shadowExpire"
	echo "shadowExpire: $NEWSHADOW"
} | tee $TMPFILE

echo
echo Apportare le modifiche? \(yes/no\)

ANS=boh

until [[ $ANS == "yes" ]]; do
	read ANS
	if [[ $ANS == "no" ]]; then clean 1; fi
done

EXITSTAT=49
while [[ $EXITSTAT -eq 49 ]]; do
	ldapmodify -x -D "$MANAGER,$BIND" -W -f $TMPFILE
	EXITSTAT=$?
done

#This line was inserted by eugen, to fix the discrepancy in the expiration date between ldap  
#and /etc/shadow (2015).
#$1 is the uid of ldap, corresponding to the username of /etc/shadow
chage -E $NEWSHADOW $1

echo Modifiche apportate. Nuova data di scadenza: "$NEWYEAR-$MONTH-$DAY".

clean $EXITSTAT

