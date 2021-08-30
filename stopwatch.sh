#!/bin/zsh


stopwatch() {
    echo "press p to pause and q to quit"
    pause=0
    dateWork=`date +%s`; 
    while true; do 
       echo -ne "$(date -u --date @$((`date +%s` - $dateWork)) +%H:%M:%S)\r";
       key=""
       key=$(bash -c "read -sn 1 -t 15 c; echo \$c")
       if [ "${key}" = "p" ]; then
           echo "";
           datePause=`date +%s`; 
           echo "${key} pressed"
           key=""
           echo "press any button to continue"
            key=$(bash -c "read -sn 1 c; echo \$c")
            dateCurr=`date +%s`; 
            diff=`expr $dateCurr - $datePause`
#           echo "pause time: $diff"
            pause=`expr $pause + $diff`
           echo -e "paused time: $(date -u --date @$((`date +%s` - $datePause)) +%H:%M:%S)\r";
            dateWork=`expr $dateWork + $diff`
       elif [ "${key}" = "q" ]; then
           echo -e "work  time: $(date -u --date @$((`date +%s` - $dateWork)) +%H:%M:%S)\r";
           echo -e "chill time: $(date -u --date @$((`date +%s` - $pause)) +%H:%M:%S)\r";
           exit 0
       fi
    done
}
