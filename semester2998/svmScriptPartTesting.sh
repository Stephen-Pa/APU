#! /bin/bash

make mode=debug product=gnu-ccac

#this test considers using the MiniBoone dataset with 1 query to test
#the individual runtimes of the algorithm

outFileTimingParts="testTimingOutputParts.txt"


echo "MiniBoon 32659 48 32768 -> algorithm after log add loop" >> $outFileTimingParts
for i in {1..100}
do
        echo "$i">> $outFileTimingParts
        ./build/debug/gsi_device_lab_3 32659 48 32768 "./MiniBoon_SVM/Full" >> $outFileTimingParts
done

