# APU
This repository presents code for a binary Radial Basis Function (RBF) Support Vector Machine (SVM) on the APU. The APU use SVM parameters from pretrained SVMs using the scikit python libray to perform an inference on queries. Datasets are obtained from the UC Irvine Machine Learning Repository and consist of the Breast Cancer Wisconsin (Diagnostic), Sports articles for objectivity analysis, MAGIC Gamma Telescope, Spambase, and MiniBooNE particle identification datasets. 

# How to Test Benchmarks

NOTE: Make sure the following are completed before continuing to run the test script:
- The machine running this test contains at least 1 APU card
- APU driverfiles are correctly installed to interface with an APU card
- Python is installed on your machine

1. From the top of the git repository, move to the semester2998 folder (EX: cd semester2998)
2. Edit the "svmTestScript.sh" file with your editor of choice. (EX: vim svmTestScript.sh)
3. Change the following variables to desired specifications:
   -> numberIterations: defines the number of trails to average execution times over
   -> svmParametersPath: specifies the location of SVM parameters (by default is included in git hub repo download, hence value is ".")
4. run the edited script. (EX: ./svmTestScript.sh)
