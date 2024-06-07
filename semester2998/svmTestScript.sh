#! /bin/bash

#Specifies how many trials to run with each test
numberIterations=2

#Specify SVM Parameters File
svmParametersPath=.


#Start Test Script
make mode=debug product=gnu-ccac

outFileTiming="testTimingOutput.txt"


#ALL GAMMA TESTS
echo "Gamma 17489 10 19020" > $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 17489 10 19020 ${parameterPath} >> $outFileTiming
done

echo "Gamma 12370 10 19020" >> $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Quarter3"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 12370 10 19020 ${parameterPath} >> $outFileTiming
done

echo "Gamma 8463 10 19020" >> $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Half"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 8463 10 19020 ${parameterPath} >> $outFileTiming
done

echo "Gamma 4298 10 19020" >> $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Quarter"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 4298 10 19020 ${parameterPath} >> $outFileTiming
done

echo "Gamma 17489 10 14265" >> $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 17489 10 14265 ${parameterPath} >> $outFileTiming
done

echo "Gamma 17489 10 9510" >> $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 17489 10 9510 ${parameterPath} >> $outFileTiming
done

echo "Gamma 17489 10 4755" >> $outFileTiming
parameterPath="${svmParametersPath}/Gamma_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 17489 10 4755 ${parameterPath} >> $outFileTiming
done

python3 parseCollectedData.py ${outFileTiming} ${numberIterations} "Gamma"

#ALL MINIBOON
echo "MiniBooNE 32659 48 100000" > $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 32659 48 100000 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 32659 48 32768" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 32659 48 32768 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 24499 48 32768" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Quarter3"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 24499 48 32768 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 16324 48 32768" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Half"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 16324 48 32768 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 8162 48 32768" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Quarter"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 8162 48 32768 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 32659 48 24576" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 32659 48 24576 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 32659 48 16384" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 32659 48 16384 ${parameterPath} >> $outFileTiming
done

echo "MiniBooNE 32659 48 8192" >> $outFileTiming
parameterPath="${svmParametersPath}/MiniBoon_SVM/Full"
for i in $(seq 1 ${numberIterations})
do
        echo "$i">> $outFileTiming
        ./build/debug/gsi_device_lab_3 32659 48 8192 ${parameterPath} >> $outFileTiming
done

python3 parseCollectedData.py ${outFileTiming} ${numberIterations} "MiniBooNE"
