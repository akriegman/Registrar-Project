#!/bin/sh

CONSTRAINTS_FILENAME="constraints_bash_test.txt"
PREFERENCES_FILENAME="prefs_bash_test.txt"
OUTPUT_FILENAME="output_bash_test.txt"

# ROOM_VALS={5..50..5}
# CLASS_VALS={10..500..10}
# PERIOD_VALS={1..10}
# STUDENT_VALS={1..3000..100}

ROOM_MAX=60
CLASS_MAX=350
PERIOD_MAX=20
STUDENT_MAX=2000


for (( NUM_ROOMS=40; NUM_ROOMS<=$ROOM_MAX; NUM_ROOMS=$NUM_ROOMS+5 ))
  do
    for (( NUM_CLASSES=50; NUM_CLASSES<=$CLASS_MAX; NUM_CLASSES=$NUM_CLASSES+50 ))
      do
        for (( NUM_PERIODS=10; NUM_PERIODS<=$PERIOD_MAX; NUM_PERIODS=$NUM_PERIODS+10 ))
          do
            for (( NUM_STUDENTS=100; NUM_STUDENTS<=$STUDENT_MAX; NUM_STUDENTS=$NUM_STUDENTS+100 ))
              do

              if [ $NUM_CLASSES \< $NUM_PERIODS*$NUM_ROOMS ]
                then
                rm $CONSTRAINTS_FILENAME
                rm $PREFERENCES_FILENAME
                rm $OUTPUT_FILENAME

                perl make_random_input.pl $NUM_ROOMS $NUM_CLASSES $NUM_PERIODS $NUM_STUDENTS $CONSTRAINTS_FILENAME $PREFERENCES_FILENAME
                python3 registrarGroupProject.py $CONSTRAINTS_FILENAME $PREFERENCES_FILENAME $OUTPUT_FILENAME

                perl is_valid.pl $CONSTRAINTS_FILENAME $PREFERENCES_FILENAME $OUTPUT_FILENAME



                # if perl is_valid.pl $CONSTRAINTS_FILENAME $PREFERENCES_FILENAME $OUTPUT_FILENAME >/dev/null | grep 'Schedule is valid' ; then
                #   perl is_valid.pl $CONSTRAINTS_FILENAME $PREFERENCES_FILENAME $OUTPUT_FILENAME
                #   exit 1
                # fi
                echo "/$(($NUM_STUDENTS*4))"
                echo ""
              fi

            done
        done
    done
done
