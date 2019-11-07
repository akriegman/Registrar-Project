#!/bin/sh
# bash run.sh constraints_testK1.txt prefs_testK1.txt output_testK1.txt
for (( i=1; i <= 6; ++i ))
do
  for (( j=1; j <= 5; ++j ))
  do
    python3 registrarGroupProject_haverford.py $1 $2 $3 $4 $i $j
  done
done
# python3 registrarGroupProject_haverford.py $1 $2 $3 $4 2 2
# perl is_valid.pl $1 $2 $3
