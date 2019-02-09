#!/bin/sh

# example
# add this to crontab -e of odoo user
# curl -sL https://gist.github.com/shingonoide/1947a97e3c00168372e950a6788ce9ad/raw/cleanup_odoo_session.sh > /tmp/cleanup_sessions.sh &&  sh /tmp/cleanup_sessions.sh 4

HOW_OLDER=${1:-6}
VERBOSE=${2:-0}
SESSION_FOLDER="$HOME/.local/share/Odoo/sessions"
TOTALFILES=$(find $SESSION_FOLDER -name '*.sess' | wc -l)
FILES2REMOVE=$(find $SESSION_FOLDER -name '*.sess' -mtime +"$HOW_OLDER")
COUNT2REMOVE=$(echo "$FILES2REMOVE" | wc -l)

for file in $FILES2REMOVE
do
  if [ "$VERBOSE" == "0" ]
  then
    rm $file
  else
    rm -v $file
  fi  
done
echo "Total $TOTALFILES files, was removed $COUNT2REMOVE files, still left $(($TOTALFILES - $COUNT2REMOVE)) files"
