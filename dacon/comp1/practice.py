
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from keras.metrics import mae

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, MaxoutDense, LSTM, LeakyReLU
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import KFold, cross_validate

from pandas.plotting import scatter_matrix
# 데이터 

train = pd.read_csv('./data/dacon/comp1/train.csv', header = 0, index_col = 0)
test = pd.read_csv('./data/dacon/comp1/test.csv', header = 0, index_col = 0)
submission = pd.read_csv('./data/dacon/comp1/sample_submission.csv', header = 0, index_col = 0)

# sns.pairplot(train, diag_kind='hist')
# plt.show()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

corr_matrix = train.corr()
hbb = corr_matrix["na"].sort_values(ascending=True)
print(hbb)

# sns.pairplot(train_dst, diag_kind='hist')


'''
# print(train.shape)         # (10000, 75)   : x_train, x_test, y_train, y_test  
# print(test.shape)          # (10000, 71)   : x_predict   71개의 컬럼으로
# print(submission.shape)    # (10000, 4)    : y_predict    아래 나머지 4개의 컬럼 (hhb, hbo2, ca, na) 을 맟춰라


# print(type(train))         # <class 'pandas.core.frame.DataFrame'>

# train.hist(bins=50, figsize=(20,20))
# plt.show()

# plt.figure(figsize=(4, 12))
# sns.heatmap(train.corr().loc['rho':'990_dst', 'hhb':].abs())


train = train.interpolate(method='values')  # 보간법  // 선형보간 
test = test.interpolate(method='values') 
# print(train.isnull().sum())  
# print(test.isnull().sum())  



train = train.fillna(method = 'bfill')   
test = test.fillna(method = 'bfill')



x_train = train.iloc[ :8000 , 38 : 71]
x_test = train.iloc [ :2000 ,  38 : 71]



y_train = train.iloc [ : 8000 , 71 : ]
y_test = train.iloc [ : 2000 , 71: ]

print(x_train.shape)  # (8000, 34)
print(x_test.shape)  # (2000, 34)

print(y_train.shape)  # (8000, 4)
print(y_test.shape)   # (2000, 4)


from sklearn.preprocessing import StandardScaler, MinMaxScaler 

# standard_scaler = StandardScaler()
# x_train = standard_scaler.fit_transform(x_train)
# x_test = standard_scaler.transform(x_test)


minmax_scaler = MinMaxScaler()
x_train = minmax_scaler.fit_transform(x_train)
x_test = minmax_scaler.transform(x_test)



# # 차원 축소

from sklearn.decomposition import PCA
from keras.metrics import mae
pca = PCA(n_components=4)
x_train = pca.fit_transform(x_train)
x_test = pca.transform(x_test)
test = pca.fit_transform(test)


# 모델

model = Sequential()

  
model.add(Dense(12,activation ='relu',input_shape=(4,)))
model.add(Dense(32,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(4))




# 훈련
early_stopping = EarlyStopping(monitor='loss', patience= 20, mode ='auto')
kfold = KFold(n_splits=5, shuffle=True) 
reduce = ReduceLROnPlateau(monitor='val_loss',factor=0.2, patience=10)

model.compile (optimizer='adam', loss = 'mae', metrics=['mae'])
hist = model.fit(x_train,y_train, verbose=1, batch_size=20, epochs= 1000, callbacks=[early_stopping, reduce], use_multiprocessing=True, validation_split=0.25)


# 평가 및 예측

loss, mse = model.evaluate(x_test,y_test, batch_size=1)
print('loss : ',loss)
print('mae : ', mae )




y_predict = model.predict(test)

print("y_predict : ", y_predict)


import matplotlib.pyplot as plt

plt.plot(hist.history['loss'])   
plt.plot(hist.history['mae'])
plt.plot(hist.history['val_mae'])
plt.plot(hist.history['val_loss'])

plt.title('loss & mae')
plt.xlabel('epoch')
plt.ylabel('loss,mae')
plt.legend(['train loss', 'test loss', 'train mae', 'test mae'])
plt.show()






# summit file 생성
# y_predict = y_predict.to_csv('./data/dacon/comp1/predict.csv', columns=['hhb','hbo2','ca','na'])
predict = pd.DataFrame(y_predict, columns=['hhb','hbo2','ca','na'])
predict.index = np.arange(10000,20000)
predict.to_csv('./data/dacon/comp1/predict.csv', index_label='id')
'''