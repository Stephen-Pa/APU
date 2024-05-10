#! /bin/bash

make mode=debug product=gnu-ccac

outFileTimingSpam="testTimingOutputSpam.txt"
outFileTimingSports="testTimingOutputSports.txt"
outFileTimingBreast="testTimingOutputBreast.txt"
outFileTimingGamma="testTimingOutputGamma.txt"
outFileTimingMiniBoon="testTimingOutputMiniBoon.txt"
outFilePower="testPowerOutput.txt"


#ALL SPAM TESTS
echo "Spam 1523 48 4601" >> $outFileTimingSpam
for i in {1..100}
do
	echo "$i">> $outFileTimingSpam
	./build/debug/gsi_device_lab_3 1523 48 4601 "./Spam_SVM/Full" >> $outFileTimingSpam
done

echo "Spam 506 48 4601" >> $outFileTimingSpam
for i in {1..100}
do      
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 506 48 4601 "./Spam_SVM/Quarter3" >> $outFileTimingSpam
done 

echo "Spam 386 48 4601" >> $outFileTimingSpam
for i in {1..100}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 386 48 4601 "./Spam_SVM/Half" >> $outFileTimingSpam
done

echo "Spam 219 48 4601" >> $outFileTimingSpam
for i in {1..100}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 219 48 4601 "./Spam_SVM/Quarter" >> $outFileTimingSpam
done

echo "Spam 1523 48 3450" >> $outFileTimingSpam
for i in {1..100}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 1523 48 3450 "./Spam_SVM/Full" >> $outFileTimingSpam
done

echo "Spam 1523 48 2300" >> $outFileTimingSpam
for i in {1..100}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 1523 48 2300 "./Spam_SVM/Full" >> $outFileTimingSpam
done

echo "Spam 1523 48 1150" >> $outFileTimingSpam
for i in {1..100}
do
        echo "$i">> $outFileTimingSpam
        ./build/debug/gsi_device_lab_3 1523 48 1150 "./Spam_SVM/Full" >> $outFileTimingSpam
done

#ALL SPORTS TESTS
echo "Sports 995 48 1000" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 1000 "./Sports_SVM/Full" >> $outFileTimingSports
done

echo "Sports 744 48 1000" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 744 48 1000 "./Sports_SVM/Quarter3" >> $outFileTimingSports
done

echo "Sports 496 48 1000" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 496 48 1000 "./Sports_SVM/Half" >> $outFileTimingSports
done

echo "Sports 248 48 1000" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 248 48 1000 "./Sports_SVM/Quarter" >> $outFileTimingSports
done

echo "Sports 995 48 750" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 750 "./Sports_SVM/Full" >> $outFileTimingSports
done

echo "Sports 995 48 500" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 500 "./Sports_SVM/Full" >> $outFileTimingSports
done

echo "Sports 995 48 250" >> $outFileTimingSports
for i in {1..100}
do
        echo "$i">> $outFileTimingSports
        ./build/debug/gsi_device_lab_3 995 48 250 "./Sports_SVM/Full" >> $outFileTimingSports
done

#ALL BREAST TESTS
echo "Breast 87 9 699" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 699 "./Breast_SVM/Full" >> $outFileTimingBreast
done

echo "Breast 22 9 699" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 22 9 699 "./Breast_SVM/Quarter3" >> $outFileTimingBreast
done

echo "Breast 17 9 699" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 17 9 699 "./Breast_SVM/Half" >> $outFileTimingBreast
done

echo "Breast 11 9 699" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 11 9 699 "./Breast_SVM/Quarter" >> $outFileTimingBreast
done

echo "Breast 87 9 524" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 524 "./Breast_SVM/Full" >> $outFileTimingBreast
done

echo "Breast 87 9 349" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 349 "./Breast_SVM/Full" >> $outFileTimingBreast
done

echo "Breast 87 9 174" >> $outFileTimingBreast
for i in {1..100}
do
        echo "$i">> $outFileTimingBreast
        ./build/debug/gsi_device_lab_3 87 9 174 "./Breast_SVM/Full" >> $outFileTimingBreast
done
#ALL GAMMA TESTS
echo "Gamma 17489 10 19020" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 19020 "./Gamma_SVM/Full" >> $outFileTimingGamma
done

echo "Gamma 12370 10 19020" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 12370 10 19020 "./Gamma_SVM/Quarter3" >> $outFileTimingGamma
done

echo "Gamma 8463 10 19020" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 8463 10 19020 "./Gamma_SVM/Half" >> $outFileTimingGamma
done

echo "Gamma 4298 10 19020" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 4298 10 19020 "./Gamma_SVM/Quarter" >> $outFileTimingGamma
done

echo "Gamma 17489 10 14265" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 14265 "./Gamma_SVM/Full" >> $outFileTimingGamma
done

echo "Gamma 17489 10 9510" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 9510 "./Gamma_SVM/Full" >> $outFileTimingGamma
done

echo "Gamma 17489 10 4755" >> $outFileTimingGamma
for i in {1..100}
do
        echo "$i">> $outFileTimingGamma
        ./build/debug/gsi_device_lab_3 17489 10 4755 "./Gamma_SVM/Full" >> $outFileTimingGamma
done
#ALL MINIBOON
echo "MiniBoon 32659 48 32768" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 32768 "./MiniBoon_SVM/Full" >> $outFileTimingMiniBoon
done

echo "MiniBoon 24499 48 32768" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 24499 48 32768 "./MiniBoon_SVM/Quarter3" >> $outFileTimingMiniBoon
done

echo "MiniBoon 16324 48 32768" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 16324 48 32768 "./MiniBoon_SVM/Half" >> $outFileTimingMiniBoon
done

echo "MiniBoon 8162 48 32768" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 8162 48 32768 "./MiniBoon_SVM/Quarter" >> $outFileTimingMiniBoon
done

echo "MiniBoon 32659 48 24576" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 24576 "./MiniBoon_SVM/Full" >> $outFileTimingMiniBoon
done

echo "MiniBoon 32659 48 16384" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 16384 "./MiniBoon_SVM/Full" >> $outFileTimingMiniBoon
done

echo "MiniBoon 32659 48 8192" >> $outFileTimingMiniBoon
for i in {1..100}
do
        echo "$i">> $outFileTimingMiniBoon
        ./build/debug/gsi_device_lab_3 32659 48 8192 "./MiniBoon_SVM/Full" >> $outFileTimingMiniBoon
done

#RUN PYTHON POWER
python3 leda.py & ./build/debug/gsi_device_lab_3 32659 48 100000 "./MiniBoon_SVM/Full" ; echo "done" >> "powerTest.txt"
