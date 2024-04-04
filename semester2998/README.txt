GENERAL INFORMATION:
This folder contains a binary classifier RBF SVM implemented on the APU

Currently, the folder contains SVM parameters for an SVM trained with the spambase dataset
-> https://archive.ics.uci.edu/dataset/94/spambase

The Orig folder is a toy example I was playing with. (scipy svm with iris dataset)
You can run that if you want, just copy the text files in place of current ones
use parameter values 66 4 20. look below for what these numbers mean.


HOW TO RUN:

1. compile code with make (Common folder not included)
2. run executable with parameters <# support vectors> <# features> <# data to classify>
-> EX: ./build/debug/gsi_device_lab3 1523 48 4601
3. output store in "output.txt"