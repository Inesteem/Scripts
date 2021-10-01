#!/bin/zsh

#TODO: catch ctrl d/c int

stopwatch() {
    echo "press p to pause and q to quit"
    pause=0
    dateWork=`date +%s`;
    pauseTime=0
    while true; do
       echo -ne "$(date -u --date @$((`date +%s` - $dateWork)) +%H:%M:%S)\r";
       key=""
       key=$(bash -c "read -sn 1 -t 15 c; echo \$c")
       if [ "${key}" = "p" ]; then
           echo "";
           datePause=`date +%s`;
           key=""
           echo "paused; press any button to continue"
            key=$(bash -c "read -sn 1 c; echo \$c")
            dateCurr=`date +%s`;
            diff=`expr $dateCurr - $datePause`
            pause=`expr $pause + $diff`
           echo -e "paused time: $(date -u --date @$((`date +%s` - $datePause)) +%H:%M:%S)\r";
            pauseTime=`expr $pauseTime + $pause`
            dateWork=`expr $dateWork + $diff`
       elif [ "${key}" = "q" ]; then
           echo -e "work  time: $(date -u --date @$((`date +%s` - $dateWork)) +%H:%M:%S)\r";
           echo -e "chill time: $(date -u --date @$pauseTime +%H:%M:%S)\r";
           return 0
       fi
    done
}
