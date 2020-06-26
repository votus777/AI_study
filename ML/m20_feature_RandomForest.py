
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


cancer = load_breast_cancer()

x_train,x_test ,y_train, y_test = train_test_split(
    cancer.data, cancer.target, shuffle = True, train_size = 0.8, random_state = 31
)


model = RandomForestClassifier(n_estimators=200 ,max_depth=4, max_features='auto')

'''
    max_features : 기본값 추천 'auto'
    n_estimators : 클수록 좋은데 메모리 많이 차지, default = 100
    n_jobs = -1 병렬처리 


'''

model.fit(x_train,y_train)


acc = model.score(x_test,y_test)


print(model.feature_importances_)
print(acc)

import matplotlib.pyplot as plt
import numpy as np
def plot_feature_importance_cancer(model):
    n_features = cancer.data.shape[1]
    plt.barh(np.arange(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), cancer.feature_names)
    plt.xlabel("Feature Importance")
    plt.ylabel("Feature")
    plt.ylim(-1, n_features)


plot_feature_importance_cancer(model)
plt.show()

