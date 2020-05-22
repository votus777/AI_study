#  keras15_mlp2.py 를 Sequential 에서 함수형으로 변경
#  Early Stopping 적용 


# 1. 데이터_________________________________
import numpy as np

x = np.array([range(1,101), range(311,411), range(100)]).T
y = np.array(range(711,811)).T




from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
   
    x, y, shuffle = False  , train_size = 0.8  
)





# 2. 모델 구성____________________________
from keras.models import Sequential, Model
from keras.layers import Dense , Input

#model -------- 1
input1 = Input(shape=(3, ), name= 'input_1') 

dense1_1 = Dense(64, activation= 'relu', name= '1_1') (input1) 
dense1_2 = Dense(24, activation='relu', name = '1_2')(dense1_1)
dense1_3 = Dense(24, activation='relu', name = '1_3')(dense1_2)
dense1_4 = Dense(48, activation='relu', name = '1_4')(dense1_3)
dense1_5 = Dense(96, activation='relu', name = '1_5')(dense1_4)



output1 = Dense  (48,name = 'output_1')(dense1_4)
output1_2 = Dense (24, name = 'output_1_2')(output1)
output1_3 = Dense (12, name = 'output_1_3')(output1_2)
output1_4 = Dense (1, name = 'output_1_4')(output1_3)


model = Model (inputs = input1, outputs= (output1_4))

# 3. KCTC 훈련 악 _______________________________________________________________________________
model.compile(loss='mse', optimizer='adam', metrics=['mse'])


from keras.callbacks import EarlyStopping
ealry_stopping= EarlyStopping(monitor='loss', patience= 10,  mode = 'auto')  

model.fit(x_train, y_train, epochs=100, batch_size = 1, validation_split= 0.5, callbacks=[ealry_stopping]) 



#4. 평가, 예측____________________________________________
loss,mse = model.evaluate(x_test, y_test, batch_size = 1) 
print("loss : ", loss)
print("mse : ", mse) 



y_predict = model.predict(x_test)
print(y_predict)


#________RMSE 구하기_________________________________________
from sklearn.metrics import mean_squared_error
def RMSE(y_test ,y_pred) :
    return np.sqrt(mean_squared_error(y_test, y_predict))

# y_test = 실제값, y_pred = 예측값

print("RMSE : ", RMSE(y_test, y_predict))    




#________R2 구하기_____________________
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)

print("R2 score : ", r2)
# _____________________________________