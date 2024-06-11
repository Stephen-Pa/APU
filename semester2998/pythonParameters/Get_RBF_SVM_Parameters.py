from ucimlrepo import fetch_ucirepo
import numpy as np
import pandas as pd
from sklearn.svm import SVC

# fetch datasets
breast_cancer_wisconsin_original = fetch_ucirepo(id=15)

spambase = fetch_ucirepo(id=94)
X_spam_temp = spambase.data.features
Y_spam_temp = spambase.data.targets

magic_gamma_telescope = fetch_ucirepo(id=159)
X_gamma_temp = magic_gamma_telescope.data.features
Y_gamma_temp = magic_gamma_telescope.data.targets


X_breast_temp = breast_cancer_wisconsin_original.data.features
Y_breast_temp = breast_cancer_wisconsin_original.data.targets

# read by default 1st sheet of an excel file
Sports_data = pd.read_excel("Book1.xlsx")

#Sports X&Y
X_Sports = np.zeros((Sports_data.shape[0],48))
Y_Sports = np.zeros(Sports_data.shape[0])
obj = Sports_data
for i in range(Sports_data.shape[0]):
    currentObj = obj.iloc[i]
    for j in range(49):
        if j == 0:
            if currentObj.iloc[0] == 'objective':
                Y_Sports[i] = 0
            elif currentObj.iloc[0] == 'subjective':
                Y_Sports[i] = 1
            else:
                exit(2998)
        else:
            X_Sports[i,j-1] = currentObj.iloc[j]

#MiniBoone
with open("MiniBooNE_PID.txt", 'r') as file:
    # Read the first line to get the numbers of classes
    num_classes = list(map(int, file.readline().strip().split()))
    Y_MiniBoon = np.zeros(num_classes[0]+num_classes[1])
    # Initialize lists to store class-wise features
    class1_features = []
    class2_features = []

    # Read the remaining lines
    for i in range(num_classes[0]):
        Y_MiniBoon[i] = 1
        line = file.readline().strip().split()
        if line:
            class1_features.append(list(map(float, line)))

    for i in range(num_classes[1]):
        line = file.readline().strip().split()
        if line:
            class2_features.append(list(map(float, line)))
temp1 = np.array(class1_features)
temp2 = np.array(class2_features)
X_MiniBoon_temp = np.concatenate((temp1,temp2), axis=0)
X_MiniBoon = np.zeros((X_MiniBoon_temp.shape[0],48))
#only have 48 features
for i in range(X_MiniBoon.shape[0]):
    for j in range(X_MiniBoon.shape[1]):
        X_MiniBoon[i,j] = X_MiniBoon_temp[i,j]


X_Sports = np.zeros((Sports_data.shape[0],48))
Y_Sports = np.zeros(Sports_data.shape[0])
obj = Sports_data
for i in range(Sports_data.shape[0]):
    currentObj = obj.iloc[i]
    for j in range(49):
        if j == 0:
            if currentObj.iloc[0] == 'objective':
                Y_Sports[i] = 0
            elif currentObj.iloc[0] == 'subjective':
                Y_Sports[i] = 1
            else:
                exit(2998)
        else:
            X_Sports[i,j-1] = currentObj.iloc[j]

#breast X
X_breast = np.zeros((X_breast_temp.shape[0],X_breast_temp.shape[1]))
obj = X_breast_temp
for i in range(X_breast_temp.shape[0]):
    currentObj = obj.iloc[i]
    for j in range(X_breast_temp.shape[1]):
        if np.isnan(currentObj.iloc[j]):
            X_breast[i, j] = 0
        else:
            X_breast[i,j] = currentObj.iloc[j]

#breast Y
Y_breast = np.zeros(Y_breast_temp.shape[0])
obj = Y_breast_temp
for i in range(Y_breast_temp.shape[0]):
    currentObj = obj.iloc[i]
    if currentObj.iloc[0] == 2:
        Y_breast[i] = 0
    elif currentObj.iloc[0] == 4:
        Y_breast[i] = 1
    else:
        exit(2998)

#gamma X
X_gamma = np.zeros((X_gamma_temp.shape[0],X_gamma_temp.shape[1]))
obj = X_gamma_temp
for i in range(X_gamma_temp.shape[0]):
    currentObj = obj.iloc[i]
    for j in range(X_gamma_temp.shape[1]):
        X_gamma[i,j] = currentObj.iloc[j]
#gamma Y
Y_gamma = np.zeros(Y_gamma_temp.shape[0])
obj = Y_gamma_temp
for i in range(Y_gamma_temp.shape[0]):
    currentObj = obj.iloc[i]
    if currentObj.iloc[0] == 'g':
        Y_gamma[i] = 0
    elif currentObj.iloc[0] == 'h':
        Y_gamma[i] = 1
    else:
        exit(2998)

#spam X
X_spam = np.zeros((X_spam_temp.shape[0],48))
obj = X_spam_temp
for i in range(X_spam_temp.shape[0]):
    currentObj = obj.iloc[i]
    for j in range(48):
        X_spam[i,j] = currentObj.iloc[j]
#spam Y
Y_spam = np.zeros(Y_spam_temp.shape[0])
obj = Y_spam_temp
for i in range(Y_spam_temp.shape[0]):
    currentObj = obj.iloc[i]
    Y_spam[i] = currentObj.iloc[0]

print("Done parsing, now training SVMs for tests")

np.random.seed(0)

#MINI DATA

random_indices = np.random.choice(len(X_MiniBoon), size=32768, replace=False)
X_MiniBoon_FULL = X_MiniBoon[random_indices]
Y_MiniBoon_FULL = Y_MiniBoon[random_indices]
random_indices = np.random.choice(len(X_MiniBoon), size=24576, replace=False)
X_MiniBoon_3Quarter = X_MiniBoon[random_indices]
Y_MiniBoon_3Quarter = Y_MiniBoon[random_indices]
random_indices = np.random.choice(len(X_MiniBoon), size=16384, replace=False)
X_MiniBoon_Half = X_MiniBoon[random_indices]
Y_MiniBoon_Half = Y_MiniBoon[random_indices]
random_indices = np.random.choice(len(X_MiniBoon), size=8192, replace=False)
X_MiniBoon_Quarter = X_MiniBoon[random_indices]
Y_MiniBoon_Quarter = Y_MiniBoon[random_indices]
print("MiniBoonFull")
# Create a RBF SVM for MiniBoonNE FULL
clf_MiniBoon_FULL = SVC(kernel='rbf', gamma=0.01)
clf_MiniBoon_FULL.fit(X_MiniBoon_FULL, Y_MiniBoon_FULL)
#get the parameters from SVM
supportVectors = clf_MiniBoon_FULL.support_vectors_
weights = clf_MiniBoon_FULL.dual_coef_
support = clf_MiniBoon_FULL.support_
intercept = clf_MiniBoon_FULL.intercept_
#put parameters in files
f = open("../MiniBoon_SVM/Full/supportVectors.txt", "w")
f2 = open("../MiniBoon_SVM/Full/supportWeights.txt", "w")
f3 = open("../MiniBoon_SVM/Full/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../MiniBoon_SVM/Full/supportGamma.txt", "w")
f3.write(str(-clf_MiniBoon_FULL.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("MiniBoon3Quarter")
# Create a RBF SVM for MiniBoonNE 3Quarter
clf_MiniBoon_3Quarter = SVC(kernel='rbf', gamma=0.01)
clf_MiniBoon_3Quarter.fit(X_MiniBoon_3Quarter, Y_MiniBoon_3Quarter)
#get the parameters from SVM
supportVectors = clf_MiniBoon_3Quarter.support_vectors_
weights = clf_MiniBoon_3Quarter.dual_coef_
support = clf_MiniBoon_3Quarter.support_
intercept = clf_MiniBoon_3Quarter.intercept_
#put parameters in files
f = open("../MiniBoon_SVM/Quarter3/supportVectors.txt", "w")
f2 = open("../MiniBoon_SVM/Quarter3/supportWeights.txt", "w")
f3 = open("../MiniBoon_SVM/Quarter3/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../MiniBoon_SVM/Quarter3/supportGamma.txt", "w")
f3.write(str(-clf_MiniBoon_3Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("MiniBoonHalf")
# Create a RBF SVM for MiniBoonNE Half
clf_MiniBoon_Half = SVC(kernel='rbf', gamma=0.01)
clf_MiniBoon_Half.fit(X_MiniBoon_Half, Y_MiniBoon_Half)
#get the parameters from SVM
supportVectors = clf_MiniBoon_Half.support_vectors_
weights = clf_MiniBoon_Half.dual_coef_
support = clf_MiniBoon_Half.support_
intercept = clf_MiniBoon_Half.intercept_
#put parameters in files
f = open("../MiniBoon_SVM/Half/supportVectors.txt", "w")
f2 = open("../MiniBoon_SVM/Half/supportWeights.txt", "w")
f3 = open("../MiniBoon_SVM/Half/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../MiniBoon_SVM/Half/supportGamma.txt", "w")
f3.write(str(-clf_MiniBoon_Half.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("MiniBoonQuarter")
# Create a RBF SVM for MiniBoonNE Quarter
clf_MiniBoon_Quarter = SVC(kernel='rbf', gamma=0.01)
clf_MiniBoon_Quarter.fit(X_MiniBoon_Quarter, Y_MiniBoon_Quarter)
#get the parameters from SVM
supportVectors = clf_MiniBoon_Quarter.support_vectors_
weights = clf_MiniBoon_Quarter.dual_coef_
support = clf_MiniBoon_Quarter.support_
intercept = clf_MiniBoon_Quarter.intercept_
#put parameters in files
f = open("../MiniBoon_SVM/Quarter/supportVectors.txt", "w")
f2 = open("../MiniBoon_SVM/Quarter/supportWeights.txt", "w")
f3 = open("../MiniBoon_SVM/Quarter/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../MiniBoon_SVM/Quarter/supportGamma.txt", "w")
f3.write(str(-clf_MiniBoon_Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
f4 = open("../MiniBoon_SVM/supportTestData.txt", "w")
#get the test data for MiniBoon
for i in range(X_MiniBoon.shape[0]):
    for j in range(X_MiniBoon.shape[1]):
        f4.write(str(X_MiniBoon[i, j]) + " ")
    f4.write("\n")
f4.close()

#SPORTS DATA

X_Sports_FULL = X_Sports
Y_Sports_FULL = Y_Sports
random_indices = np.random.choice(len(X_Sports), size=746, replace=False)
X_Sports_3Quarter = X_Sports[random_indices]
Y_Sports_3Quarter = Y_Sports[random_indices]
random_indices = np.random.choice(len(X_Sports), size=497, replace=False)
X_Sports_Half = X_Sports[random_indices]
Y_Sports_Half = Y_Sports[random_indices]
random_indices = np.random.choice(len(X_Sports), size=248, replace=False)
X_Sports_Quarter = X_Sports[random_indices]
Y_Sports_Quarter = Y_Sports[random_indices]
print("SportsFull")
# Create a RBF SVM for Sports FULL
clf_Sports_FULL = SVC(kernel='rbf', gamma=0.01)
clf_Sports_FULL.fit(X_Sports_FULL, Y_Sports_FULL)
#get the parameters from SVM
supportVectors = clf_Sports_FULL.support_vectors_
weights = clf_Sports_FULL.dual_coef_
support = clf_Sports_FULL.support_
intercept = clf_Sports_FULL.intercept_
#put parameters in files
f = open("../Sports_SVM/Full/supportVectors.txt", "w")
f2 = open("../Sports_SVM/Full/supportWeights.txt", "w")
f3 = open("../Sports_SVM/Full/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Sports_SVM/Full/supportGamma.txt", "w")
f3.write(str(-clf_Sports_FULL.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("Sports3Quarter")
# Create a RBF SVM for Sports 3Quarter
clf_Sports_3Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Sports_3Quarter.fit(X_Sports_3Quarter, Y_Sports_3Quarter)
#get the parameters from SVM
supportVectors = clf_Sports_3Quarter.support_vectors_
weights = clf_Sports_3Quarter.dual_coef_
support = clf_Sports_3Quarter.support_
intercept = clf_Sports_3Quarter.intercept_
#put parameters in files
f = open("../Sports_SVM/Quarter3/supportVectors.txt", "w")
f2 = open("../Sports_SVM/Quarter3/supportWeights.txt", "w")
f3 = open("../Sports_SVM/Quarter3/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Sports_SVM/Quarter3/supportGamma.txt", "w")
f3.write(str(-clf_Sports_3Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("SportsHalf")
# Create a RBF SVM for Sports Half
clf_Sports_Half = SVC(kernel='rbf', gamma=0.01)
clf_Sports_Half.fit(X_Sports_Half, Y_Sports_Half)
#get the parameters from SVM
supportVectors = clf_Sports_Half.support_vectors_
weights = clf_Sports_Half.dual_coef_
support = clf_Sports_Half.support_
intercept = clf_Sports_Half.intercept_
#put parameters in files
f = open("../Sports_SVM/Half/supportVectors.txt", "w")
f2 = open("../Sports_SVM/Half/supportWeights.txt", "w")
f3 = open("../Sports_SVM/Half/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Sports_SVM/Half/supportGamma.txt", "w")
f3.write(str(-clf_Sports_Half.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("SportsQuarter")
# Create a RBF SVM for Sports Quarter
clf_Sports_Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Sports_Quarter.fit(X_Sports_Quarter, Y_Sports_Quarter)
#get the parameters from SVM
supportVectors = clf_Sports_Quarter.support_vectors_
weights = clf_Sports_Quarter.dual_coef_
support = clf_Sports_Quarter.support_
intercept = clf_Sports_Quarter.intercept_
#put parameters in files
f = open("../Sports_SVM/Quarter/supportVectors.txt", "w")
f2 = open("../Sports_SVM/Quarter/supportWeights.txt", "w")
f3 = open("../Sports_SVM/Quarter/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Sports_SVM/Quarter/supportGamma.txt", "w")
f3.write(str(-clf_Sports_Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
f4 = open("../Sports_SVM/supportTestData.txt", "w")
#get the test data (queries)
for i in range(X_Sports.shape[0]):
    for j in range(X_Sports.shape[1]):
        f4.write(str(X_Sports[i, j]) + " ")
    f4.write("\n")
f4.close()

#BREAST CANCER DATA

X_Breast_FULL = X_breast
Y_Breast_FULL = Y_breast
random_indices = np.random.choice(len(X_breast), size=65, replace=False)
X_Breast_3Quarter = X_breast[random_indices]
Y_Breast_3Quarter = Y_breast[random_indices]
random_indices = np.random.choice(len(X_breast), size=43, replace=False)
X_Breast_Half = X_breast[random_indices]
Y_Breast_Half = Y_breast[random_indices]
random_indices = np.random.choice(len(X_breast), size=21, replace=False)
X_Breast_Quarter = X_breast[random_indices]
Y_Breast_Quarter = Y_breast[random_indices]
print("BreastFull")
# Create a RBF SVM for Breast FULL
clf_Breast_FULL = SVC(kernel='rbf', gamma=0.01)
clf_Breast_FULL.fit(X_Breast_FULL, Y_Breast_FULL)
#get the parameters from SVM
supportVectors = clf_Breast_FULL.support_vectors_
weights = clf_Breast_FULL.dual_coef_
support = clf_Breast_FULL.support_
intercept = clf_Breast_FULL.intercept_
#put parameters in files
f = open("../Breast_SVM/Full/supportVectors.txt", "w")
f2 = open("../Breast_SVM/Full/supportWeights.txt", "w")
f3 = open("../Breast_SVM/Full/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Breast_SVM/Full/supportGamma.txt", "w")
f3.write(str(-clf_Breast_FULL.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("Breast3Quarter")
# Create a RBF SVM for Breast 3Quarter
clf_Breast_3Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Breast_3Quarter.fit(X_Breast_3Quarter, Y_Breast_3Quarter)
#get the parameters from SVM
supportVectors = clf_Breast_3Quarter.support_vectors_
weights = clf_Breast_3Quarter.dual_coef_
support = clf_Breast_3Quarter.support_
intercept = clf_Breast_3Quarter.intercept_
#put parameters in files
f = open("../Breast_SVM/Quarter3/supportVectors.txt", "w")
f2 = open("../Breast_SVM/Quarter3/supportWeights.txt", "w")
f3 = open("../Breast_SVM/Quarter3/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Breast_SVM/Quarter3/supportGamma.txt", "w")
f3.write(str(-clf_Breast_3Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("BreastHalf")
# Create a RBF SVM for Breast Half
clf_Breast_Half = SVC(kernel='rbf', gamma=0.01)
clf_Breast_Half.fit(X_Breast_Half, Y_Breast_Half)
#get the parameters from SVM
supportVectors = clf_Breast_Half.support_vectors_
weights = clf_Breast_Half.dual_coef_
support = clf_Breast_Half.support_
intercept = clf_Breast_Half.intercept_
#put parameters in files
f = open("../Breast_SVM/Half/supportVectors.txt", "w")
f2 = open("../Breast_SVM/Half/supportWeights.txt", "w")
f3 = open("../Breast_SVM/Half/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Breast_SVM/Half/supportGamma.txt", "w")
f3.write(str(-clf_Breast_Half.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("BreastQuarter")
# Create a RBF SVM for Breast Quarter
clf_Breast_Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Breast_Quarter.fit(X_Breast_Quarter, Y_Breast_Quarter)
#get the parameters from SVM
supportVectors = clf_Breast_Quarter.support_vectors_
weights = clf_Breast_Quarter.dual_coef_
support = clf_Breast_Quarter.support_
intercept = clf_Breast_Quarter.intercept_
#put parameters in files
f = open("../Breast_SVM/Quarter/supportVectors.txt", "w")
f2 = open("../Breast_SVM/Quarter/supportWeights.txt", "w")
f3 = open("../Breast_SVM/Quarter/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Breast_SVM/Quarter/supportGamma.txt", "w")
f3.write(str(-clf_Breast_Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
f4 = open("../Breast_SVM/supportTestData.txt", "w")
#get the test data (queries)
for i in range(X_breast.shape[0]):
    for j in range(X_breast.shape[1]):
        f4.write(str(X_breast[i, j]) + " ")
    f4.write("\n")
f4.close()

#SPAM DATA

X_Spam_FULL = X_spam
Y_Spam_FULL = Y_spam
random_indices = np.random.choice(len(X_spam), size=1142, replace=False)
X_Spam_3Quarter = X_spam[random_indices]
Y_Spam_3Quarter = Y_spam[random_indices]
random_indices = np.random.choice(len(X_spam), size=761, replace=False)
X_Spam_Half = X_spam[random_indices]
Y_Spam_Half = Y_spam[random_indices]
random_indices = np.random.choice(len(X_spam), size=380, replace=False)
X_Spam_Quarter = X_spam[random_indices]
Y_Spam_Quarter = Y_spam[random_indices]
print("SpamFull")
# Create a RBF SVM for Spam FULL
clf_Spam_FULL = SVC(kernel='rbf', gamma=0.01)
clf_Spam_FULL.fit(X_Spam_FULL, Y_Spam_FULL)
#get the parameters from SVM
supportVectors = clf_Spam_FULL.support_vectors_
weights = clf_Spam_FULL.dual_coef_
support = clf_Spam_FULL.support_
intercept = clf_Spam_FULL.intercept_
#put parameters in files
f = open("../Spam_SVM/Full/supportVectors.txt", "w")
f2 = open("../Spam_SVM/Full/supportWeights.txt", "w")
f3 = open("../Spam_SVM/Full/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Spam_SVM/Full/supportGamma.txt", "w")
f3.write(str(-clf_Spam_FULL.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("Spam3Quarter")
# Create a RBF SVM for Spam 3Quarter
clf_Spam_3Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Spam_3Quarter.fit(X_Spam_3Quarter, Y_Spam_3Quarter)
#get the parameters from SVM
supportVectors = clf_Spam_3Quarter.support_vectors_
weights = clf_Spam_3Quarter.dual_coef_
support = clf_Spam_3Quarter.support_
intercept = clf_Spam_3Quarter.intercept_
#put parameters in files
f = open("../Spam_SVM/Quarter3/supportVectors.txt", "w")
f2 = open("../Spam_SVM/Quarter3/supportWeights.txt", "w")
f3 = open("../Spam_SVM/Quarter3/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Spam_SVM/Quarter3/supportGamma.txt", "w")
f3.write(str(-clf_Spam_3Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("SpamHalf")
# Create a RBF SVM for Spam Half
clf_Spam_Half = SVC(kernel='rbf', gamma=0.01)
clf_Spam_Half.fit(X_Spam_Half, Y_Spam_Half)
#get the parameters from SVM
supportVectors = clf_Spam_Half.support_vectors_
weights = clf_Spam_Half.dual_coef_
support = clf_Spam_Half.support_
intercept = clf_Spam_Half.intercept_
#put parameters in files
f = open("../Spam_SVM/Half/supportVectors.txt", "w")
f2 = open("../Spam_SVM/Half/supportWeights.txt", "w")
f3 = open("../Spam_SVM/Half/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Spam_SVM/Half/supportGamma.txt", "w")
f3.write(str(-clf_Spam_Half.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("SpamQuarter")
# Create a RBF SVM for Spam Quarter
clf_Spam_Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Spam_Quarter.fit(X_Spam_Quarter, Y_Spam_Quarter)
#get the parameters from SVM
supportVectors = clf_Spam_Quarter.support_vectors_
weights = clf_Spam_Quarter.dual_coef_
support = clf_Spam_Quarter.support_
intercept = clf_Spam_Quarter.intercept_
#put parameters in files
f = open("../Spam_SVM/Quarter/supportVectors.txt", "w")
f2 = open("../Spam_SVM/Quarter/supportWeights.txt", "w")
f3 = open("../Spam_SVM/Quarter/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Spam_SVM/Quarter/supportGamma.txt", "w")
f3.write(str(-clf_Spam_Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
f4 = open("../Spam_SVM/supportTestData.txt", "w")
#get the test data (queries)
for i in range(X_spam.shape[0]):
    for j in range(X_spam.shape[1]):
        f4.write(str(X_spam[i, j]) + " ")
    f4.write("\n")
f4.close()

#GAMMA DATA

X_Gamma_FULL = X_gamma
Y_Gamma_FULL = Y_gamma
random_indices = np.random.choice(len(X_gamma), size=13116, replace=False)
X_Gamma_3Quarter = X_gamma[random_indices]
Y_Gamma_3Quarter = Y_gamma[random_indices]
random_indices = np.random.choice(len(X_gamma), size=8744, replace=False)
X_Gamma_Half = X_gamma[random_indices]
Y_Gamma_Half = Y_gamma[random_indices]
random_indices = np.random.choice(len(X_gamma), size=4372, replace=False)
X_Gamma_Quarter = X_gamma[random_indices]
Y_Gamma_Quarter = Y_gamma[random_indices]
print("GammaFull")
# Create a RBF SVM for Gamma FULL
clf_Gamma_FULL = SVC(kernel='rbf', gamma=0.01)
clf_Gamma_FULL.fit(X_Gamma_FULL, Y_Gamma_FULL)
#get the parameters from SVM
supportVectors = clf_Gamma_FULL.support_vectors_
weights = clf_Gamma_FULL.dual_coef_
support = clf_Gamma_FULL.support_
intercept = clf_Gamma_FULL.intercept_
#put parameters in files
f = open("../Gamma_SVM/Full/supportVectors.txt", "w")
f2 = open("../Gamma_SVM/Full/supportWeights.txt", "w")
f3 = open("../Gamma_SVM/Full/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Gamma_SVM/Full/supportGamma.txt", "w")
f3.write(str(-clf_Gamma_FULL.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("Gamma3Quarter")
# Create a RBF SVM for Gamma 3Quarter
clf_Gamma_3Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Gamma_3Quarter.fit(X_Gamma_3Quarter, Y_Gamma_3Quarter)
#get the parameters from SVM
supportVectors = clf_Gamma_3Quarter.support_vectors_
weights = clf_Gamma_3Quarter.dual_coef_
support = clf_Gamma_3Quarter.support_
intercept = clf_Gamma_3Quarter.intercept_
#put parameters in files
f = open("../Gamma_SVM/Quarter3/supportVectors.txt", "w")
f2 = open("../Gamma_SVM/Quarter3/supportWeights.txt", "w")
f3 = open("../Gamma_SVM/Quarter3/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Gamma_SVM/Quarter3/supportGamma.txt", "w")
f3.write(str(-clf_Gamma_3Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("GammaHalf")
# Create a RBF SVM for Gamma Half
clf_Gamma_Half = SVC(kernel='rbf', gamma=0.01)
clf_Gamma_Half.fit(X_Gamma_Half, Y_Gamma_Half)
#get the parameters from SVM
supportVectors = clf_Gamma_Half.support_vectors_
weights = clf_Gamma_Half.dual_coef_
support = clf_Gamma_Half.support_
intercept = clf_Gamma_Half.intercept_
#put parameters in files
f = open("../Gamma_SVM/Half/supportVectors.txt", "w")
f2 = open("../Gamma_SVM/Half/supportWeights.txt", "w")
f3 = open("../Gamma_SVM/Half/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Gamma_SVM/Half/supportGamma.txt", "w")
f3.write(str(-clf_Gamma_Half.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
print("GammaQuarter")
# Create a RBF SVM for Spam Quarter
clf_Gamma_Quarter = SVC(kernel='rbf', gamma=0.01)
clf_Gamma_Quarter.fit(X_Gamma_Quarter, Y_Gamma_Quarter)
#get the parameters from SVM
supportVectors = clf_Gamma_Quarter.support_vectors_
weights = clf_Gamma_Quarter.dual_coef_
support = clf_Gamma_Quarter.support_
intercept = clf_Gamma_Quarter.intercept_
#put parameters in files
f = open("../Gamma_SVM/Quarter/supportVectors.txt", "w")
f2 = open("../Gamma_SVM/Quarter/supportWeights.txt", "w")
f3 = open("../Gamma_SVM/Quarter/supportIntercept.txt", "w")
f3.write(str(intercept[0]))
f3.close()
f3 = open("../Gamma_SVM/Quarter/supportGamma.txt", "w")
f3.write(str(-clf_Gamma_Quarter.gamma))
f3.close()
for i in range(supportVectors.shape[0]):
    for j in range(supportVectors.shape[1]):
        f.write(str(supportVectors[i, j])+" ")
    f2.write(str(weights[0,i]) + "\n")
    f.write("\n")
f.close()
f2.close()
f4 = open("../Gamma_SVM/supportTestData.txt", "w")
#get the test data (queries)
for i in range(X_gamma.shape[0]):
    for j in range(X_gamma.shape[1]):
        f4.write(str(X_gamma[i, j]) + " ")
    f4.write("\n")
f4.close()