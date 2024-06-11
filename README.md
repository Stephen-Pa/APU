# APU
This repository presents code for a binary Radial Basis Function (RBF) Support Vector Machine (SVM) on the APU. The APU use SVM parameters from pretrained SVMs using the scikit python libray to perform an inference on queries. Datasets are obtained from the UC Irvine Machine Learning Repository and consist of the Breast Cancer Wisconsin (Diagnostic), Sports articles for objectivity analysis, MAGIC Gamma Telescope, Spambase, and MiniBooNE particle identification datasets. 

# Python Files

The RBF SVM implemented is based off the RBF SVM in scikit. The /semester2998/pythonParameters folder provides python code that displays the use of the scikit RBF SVM and how it functions.

NOTE: make sure all python dependencies are installed before executing any files. These dependencies are found in pythonPackages.txt in the /semester2998/pythonParameters folder.

All python files can be run by executing python files normally without any arguments (EX: python3 RBF_SVM_scikit.py)

RBF_SVM_scikit.py -> scikit toy example to show how RBF SVM works
RBF_SVM_Check_Inference.py -> uses trained scikit RBF SVM to extract parameters and recreates inference manually
Get_RBF_SVM_Parameters.py -> recreates RBF SVM parameter text files for uploading to the APU 


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
