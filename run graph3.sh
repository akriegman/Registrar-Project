#!/bin/sh
# bash run.sh haverfordConstraints.txt haverfordStudentPrefs.txt haverford_output.txt
for (( i=0; i <= 12 * 4; ++i ))
do
  # let "s = 12 - $i * 15/60"
  # let "f = 12 + $i * 15/60"
  s=$(bc <<< "scale=2;12 - $i * 15/60")
  f=$(bc <<< "scale=2;12 + $i * 15/60")
  echo $s
  echo $f
  python3 registrarGroupProject_haverford.py $1 $2 $3 $4 $s $f
done
# perl is_valid.pl $1 $2 $3
