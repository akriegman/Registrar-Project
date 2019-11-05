#!/bin/sh
# bash run.sh constraints_testK1.txt prefs_testK1.txt output_testK1.txt
for (( i=6; i <= 18; ++i ))
do
  for (( j=$i; j <= 19; ++j ))
  do
    python3 registrarGroupProject_haverford.py $1 $2 $3 $4 $i $j
  done
done
# perl is_valid.pl $1 $2 $3
