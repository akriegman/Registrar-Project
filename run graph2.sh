#!/bin/sh
# bash run.sh constraints_testK1.txt prefs_testK1.txt output_testK1.txt
for (( i=6; i <= 18; ++i ))
do
  let "j = $i + 1"
  echo $j
  python3 registrarGroupProject_haverford.py $1 $2 $3 $4 $i $j
done
# perl is_valid.pl $1 $2 $3
