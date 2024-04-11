#! /bin/bash

outFileTimingSpam = "testTimingOutputSpam.txt"
outFileTimingSports = "testTimingOutputSports.txt"
outFileTimingBreast = "testTimingOutputBreast.txt"
outFileTimingGamma = "testTimingOutputGamma.txt"
outFileTimingMiniBoon = "testTimingOutputMiniBoon.txt"


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