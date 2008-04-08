#!/bin/bash

if [ "$1" == "" ]; then
    exit 1
fi

nc localhost 4000 <<EOF
auth admin whatever
dllink $1
exit
EOF

#mocp -p /usr/share/sounds/question.wav
python -c "import syslog; syslog.openlog('ed2k',0,syslog.LOG_USER); syslog.syslog(syslog.LOG_INFO, '$1'); syslog.closelog()"
    
