import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


iris = load_iris()
X = iris.data
y = iris.target

X_2d = X[:, :4]
X_2d = X_2d[y > 0]
y_2d = y[y > 0]
y_2d -= 1

X_train, X_test, y_train, y_test = train_test_split(X_2d,y_2d,test_size=0.2, random_state=0)

# Create a RBF SVM classifier with gamma=0.1
clf = SVC(kernel='rbf', gamma=0.01)

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Predict the labels of the testing data
y_pred = clf.predict(X_test)


#get the predicted output
predictArray = np.zeros(X_test.shape[0])
#get the parameters of the model that was trained
supportVectors = clf.support_vectors_
weights = clf.dual_coef_
support = clf.support_
intercept = clf.intercept_


#Expected values to get out of the RBF SVM inference with X values
decision_function = clf.decision_function(X_test)

#recreate inference
decision_array_manual = np.zeros(X_test.shape[0]).astype('float64')
#manual inference
for i in range(X_test.shape[0]):
    globalSum = 0
    for j in range(supportVectors.shape[0]):
        localSum=0
        #get the squared euclidean distance for one query
        for z in range(supportVectors.shape[1]):
            localSum += (supportVectors[j,z] - X_test[i,z])**2
        #plug the squared eclidean distance into the kernel function
        #multiply by the weight and add to a global sum
        globalSum += (weights[0, j] * np.exp(-clf.gamma * localSum))
    #finished evaluating kernel function with each support vector
    #finally add in intercept value and classify
    globalSum+=intercept
    decision_array_manual[i] = globalSum.item()
    if globalSum > 0:
        predictArray[i] = 1
    else:
        predictArray[i] = 0

flag = 1
for i in range(X_test.shape[0]):
    if (decision_array_manual[i] - decision_function[i]) > .01:
        print("Value at entry: "+str(i)+" is not correct!")
        print("Manual calculated value: "+str(decision_array_manual[i])+" scikit calculated value: "+str(decision_function[i]))
        flag=0

if flag:
    print("Manual calculation does not produce errors!")