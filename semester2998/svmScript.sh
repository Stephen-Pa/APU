#! /bin/bash

outFileTimingSpam = "testTimingOutputSpam.txt"
outFileTimingSports = "testTimingOutputSports.txt"
outFileTimingBreast = "testTimingOutputBreast.txt"
outFileTimingGamma = "testTimingOutputGamma.txt"
outFileTimingMiniBoon = "testTimingOutputMiniBoon.txt"
outFilePower = "testPowerOutput.txt"


#ALL SPAM TESTS
echo "Spam 1523 48 4601" >> $outFileTimingSpam
for i in {1..1000}
do
	echo "$i">> $outFileTimingSpam
	./build/debug/gsi_device_lab_3 1523 48 4601 "./Spam_SVM/Full"
done

echo "Spam 506 48 4601" >> $outFileTimingSpam
for i in {1..1000}
do      
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 506 48 4601 "./Spam_SVM/Quarter3"
done 

echo "Spam 386 48 4601" >> $outFileTimingSpam
for i in {1..1000}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 386 48 4601 "./Spam_SVM/Half"
done

echo "Spam 219 48 4601" >> $outFileTimingSpam
for i in {1..1000}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 219 48 4601 "./Spam_SVM/Quarter"
done

echo "Spam 1523 48 3450" >> $outFileTimingSpam
for i in {1..1000}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 1523 48 3450 "./Spam_SVM/Full"
done

echo "Spam 1523 48 2300" >> $outFileTimingSpam
for i in {1..1000}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 1523 48 2300 "./Spam_SVM/Full"
done

echo "Spam 1523 48 1150" >> $outFileTimingSpam
for i in {1..1000}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 1523 48 1150 "./Spam_SVM/Full"
done

#ALL SPORTS TESTS
echo "Sports 995 48 1000" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 1000 "./Sports_SVM/Full"
done

echo "Sports 744 48 1000" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 744 48 1000 "./Sports_SVM/Quarter3"
done

echo "Sports 496 48 1000" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 496 48 1000 "./Sports_SVM/Half"
done

echo "Sports 248 48 1000" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 248 48 1000 "./Sports_SVM/Quarter"
done

echo "Sports 995 48 750" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 750 "./Sports_SVM/Full"
done

echo "Sports 995 48 500" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 500 "./Sports_SVM/Full"
done

echo "Sports 995 48 250" >> $outFileTimingSports
for i in {1..1000}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 250 "./Sports_SVM/Full"
done

#ALL BREAST TESTS
echo "Breast 87 9 699" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 699 "./Breast_SVM/Full"
done

echo "Breast 22 9 699" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 22 9 699 "./Breast_SVM/Quarter3"
done

echo "Breast 17 9 699" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 17 9 699 "./Breast_SVM/Half"
done

echo "Breast 11 9 699" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 11 9 699 "./Breast_SVM/Quarter"
done

echo "Breast 87 9 524" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 524 "./Breast_SVM/Full"
done

echo "Breast 87 9 349" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 349 "./Breast_SVM/Full"
done

echo "Breast 87 9 174" >> $outFileTimingBreast
for i in {1..1000}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 174 "./Breast_SVM/Full"
done
#ALL GAMMA TESTS
echo "Gamma 17489 10 19020" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 19020 "./Gamma_SVM/Full"
done

echo "Gamma 12730 10 19020" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 12730 10 19020 "./Gamma_SVM/Quarter3"
done

echo "Gamma 8463 10 19020" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 8463 10 19020 "./Gamma_SVM/Half"
done

echo "Gamma 4298 10 19020" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 4298 10 19020 "./Gamma_SVM/Quarter"
done

echo "Gamma 17489 10 14265" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 14265 "./Gamma_SVM/Full"
done

echo "Gamma 17489 10 9510" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 9510 "./Gamma_SVM/Full"
done

echo "Gamma 17489 10 4755" >> $outFileTimingGamma
for i in {1..1000}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 4755 "./Gamma_SVM/Full"
done
#ALL MINIBOON
echo "MiniBoon 32659 48 32768" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 32768 "./MiniBoon_SVM/Full"
done

echo "MiniBoon 24499 48 32768" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 24499 48 32768 "./MiniBoon_SVM/Quarter3"
done

echo "MiniBoon 16324 48 32768" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 16324 48 32768 "./MiniBoon_SVM/Half"
done

echo "MiniBoon 8162 48 32768" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 8162 48 32768 "./MiniBoon_SVM/Quarter"
done

echo "MiniBoon 32659 48 24576" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 24576 "./MiniBoon_SVM/Full"
done

echo "MiniBoon 32659 48 16384" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 16384 "./MiniBoon_SVM/Full"
done

echo "MiniBoon 32659 48 8192" >> $outFileTimingMiniBoon
for i in {1..1000}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 8192 "./MiniBoon_SVM/Full"
done

#RUN PYTHON POWER
python3 leda.py & ./build/debug/gsi_device_lab_3 32659 48 100000 "./MiniBoon_SVM/Full" ; echo "done" >> "powerTest.txt"
