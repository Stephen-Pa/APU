#! /bin/bash

make mode=debug product=gnu-ccac

outFilePower="testPowerOutput.txt"

#RUN PYTHON POWER
for i in {1..200}
do
	echo "New Test">> $outFilePower
	python3 leda.py & ./build/debug/gsi_device_lab_3 32659 48 100000 "./MiniBoon_SVM/Full"
done
