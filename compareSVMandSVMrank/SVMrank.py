import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,f1_score,recall_score,precision_score
from r_train import r_train
from r_predict import r_predict
from sklearn.metrics import roc_curve, auc
import time
start_time = time.time()
# data = pd.read_csv('../data software defect prediction/dataEclipse/file/eclipse-metrics-files-2.0.csv ')
# X = data.iloc[:, 5:]
# y = data.iloc[:, 3]
# encoder_y = LabelEncoder()
# y = encoder_y.fit_transform(y)
# a = 0
# b = 0
# status = []
# for i in y:
#     if i > 0:
#         status.append(1)
#         a = a + 1
#     else:
#         status.append(0)
#         b = b + 1
# y = np.array(status)
# X = X.to_numpy()
# # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=3, shuffle=bool)
# accuracy=0
# f1=0
# recall=0
# precision=0
# #K-fold:
# kf = KFold(n_splits=10)
# kf.get_n_splits(X)
# for train_index, test_index in kf.split(X):
#     X_trainf, X_testf = X[train_index], X[test_index]
#     y_trainf, y_testf = y[train_index], y[test_index]
#     # classifier2 = SVC(kernel='rbf')
#     # classifier2.fit(X_trainf, y_trainf)
#     mohinh = r_train(X_trainf, y_trainf)
#     y_pred_svm = r_predict(mohinh,X_testf)
#     accuracy+= accuracy_score(y_testf,y_pred_svm)/10.0
#     f1+= f1_score(y_testf,y_pred_svm)/10.0
#     recall+= recall_score(y_testf,y_pred_svm)/10.0
#     precision+=precision_score(y_testf,y_pred_svm)/10.0
#     print(y_testf)
#     print(y_pred_svm)
#     print(accuracy_score(y_testf,y_pred_svm))
#     print(recall_score(y_testf,y_pred_svm))
#     print(precision_score(y_testf,y_pred_svm))
#     print(f1_score(y_testf,y_pred_svm))
#
# print('accuary = ',accuracy)
# print('recall = ',recall)
# print('precision = ',precision)
# print('f1 = ',f1)
data = pd.read_csv('../data software defect prediction/dataApache(PROMISE)/xalan-2.5.csv')

X_train = data.iloc[:, 1:21]
y_train = data.iloc[:, 21]
encoder_y = LabelEncoder()
y_train = encoder_y.fit_transform(y_train)

status = []
for i in y_train:
    if i > 0:
        status.append(1)
    else:
        status.append(0)
y_train = np.array(status)
X_train = X_train.to_numpy()
data = pd.read_csv('../data software defect prediction/dataApache(PROMISE)/xalan-2.6.csv')

X_test = data.iloc[:, 1:21]
y_test = data.iloc[:, 21]
encoder_y = LabelEncoder()
y_test = encoder_y.fit_transform(y_test)

status = []
for i in y_test:
    if i > 0:
        status.append(1)

    else:
        status.append(0)

y_test = np.array(status)
X_test = X_test.to_numpy()
mohinh = r_train(X_train, y_train)
y_pred_svm = r_predict(mohinh,X_test)
print(y_test)
svm_fpr, svm_tpr, threshold = roc_curve(y_test,y_pred_svm)
auc_svm= auc(svm_fpr,svm_tpr)
print(auc_svm)
end_time = time.time()
elapsed_time = end_time - start_time
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
