#!/bin/sh
# bash run.sh constraints_testK1.txt prefs_testK1.txt output_testK1.txt
for (( i=0; i <= 1000; ++i ))
do
  echo number of courses: $(( 350 + $(( 1000*$i )) ))
  perl make_random_input.pl $(( 50 + $(( 100*$i )) )) $(( 350 + $(( 1000*$i )) )) $(( 60 + $(( 100*$i )) )) $(( 1177 + $(( 100*$i )) )) timeAnalCons$i.txt timeAnalPrefs$i.txt
  STARTTIME=$(date +%s)
  #command block that takes time to complete...
  python3 registrarGroupProject.py timeAnalCons$i.txt timeAnalPrefs$i.txt timeAnalOut$i.txt
  ENDTIME=$(date +%s)
  echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."
done
# perl is_valid.pl $1 $2 $3
