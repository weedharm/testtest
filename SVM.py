import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,f1_score,recall_score,precision_score
from sklearn.metrics import roc_curve, auc
# importing dataset
data = pd.read_csv('camel-1.2.csv ')
X = data.iloc[:,1:-1].values
data.bug = data.bug.apply(lambda x: 1 if x > 0 else 0) 
y = data.iloc[:,-1].values
# data = pd.read_csv('../data software defect prediction/dataApache(PROMISE)/camel-1.2.csv ')
#
# X_test = data.iloc[:, 1:21]
# y_test = data.iloc[:, 21]
# encoder_y = LabelEncoder()
# y_test = encoder_y.fit_transform(y_test)
# a = 0
# b = 0
# status = []
# for i in y_test:
#     if i > 0:
#         status.append(1)
#         a = a + 1
#     else:
#         status.append(0)
#         b = b + 1
# y_test = np.array(status)
# X_test = X_test.to_numpy()
# print(X_train,len(X_train))
# print(y_train,len(y_train))
# print(X_test,len(X_test))
# print(y_test,len(y_test))
# classifier2 = SVC(kernel='rbf')
# classifier2.fit(X_train, y_train)
# y_pred= classifier2.predict(X_test)
# y_pred_svm = classifier2.decision_function(X_test)
# print(y_pred_svm,len(y_pred_svm))
# print(y_pred,len(y_pred))
# svm_fpr, svm_tpr, threshold = roc_curve(y_test,y_pred_svm, pos_label=2)
# auc_svm= auc(svm_fpr,svm_tpr)
# print(auc_svm)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=bool)
accuracy=0
f1=0
recall=0
precision=0
#K-fold:
kf = KFold(n_splits=10)
kf.get_n_splits(X)
for train_index, test_index in kf.split(X):
    X_trainf, X_testf = X[train_index], X[test_index]
    y_trainf, y_testf = y[train_index], y[test_index]
    classifier2 = SVC(kernel='rbf')
    classifier2.fit(X_trainf, y_trainf)
    y_pred_svm = classifier2.predict(X_testf)
    accuracy+= accuracy_score(y_testf,y_pred_svm)/10.0
    f1+= f1_score(y_testf,y_pred_svm)/10.0
    recall+= recall_score(y_testf,y_pred_svm)/10.0
    precision+=precision_score(y_testf,y_pred_svm)/10.0
print('acc=',accuracy)
print('pre=',precision)
print('recall=',recall)
print('f1=',f1)
#     print(y_testf)
#     print(y_pred_svm)
#     print(accuracy_score(y_testf,y_pred_svm))
#     print(recall_score(y_testf,y_pred_svm))
#     print(precision_score(y_testf,y_pred_svm))
#     print(f1_score(y_testf,y_pred_svm))

# print('accuary = ',accuracy)
# print('recall = ',recall)
# print('precision = ',precision)
# print('f1 = ',f1)
# classifier2 = SVC(kernel='rbf')
# classifier2.fit(X_train, y_train)
# y_pred_svm = classifier2.predict(X_test)
# print(accuracy_score(y_test,y_pred_svm))
# print(precision_score(y_test,y_pred_svm))
# print(recall_score(y_test,y_pred_svm))
# print(X_train)
# print(y_train)
# print(X_test)
# print(y_test)
# print(y_pred_svm)