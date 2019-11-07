#!/bin/sh
# bash run.sh constraints_testK1.txt prefs_testK1.txt output_testK1.txt
for (( i=1; i <= 100; ++i ))
do
  python3 registrarGroupProject_haverford.py $1 $2 $3 3
done
# python3 registrarGroupProject_haverford.py $1 $2 $3 $4 2 2
# perl is_valid.pl $1 $2 $3
