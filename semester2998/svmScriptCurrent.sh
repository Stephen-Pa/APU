#! /bin/bash

make mode=debug product=gnu-ccac

outFileTimingGamma="testTimingOutputGamma.txt"

echo "Gamma 12730 10 19020" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 12730 10 19020 "./Gamma_SVM/Quarter3"
done
