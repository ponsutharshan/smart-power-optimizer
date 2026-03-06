import pandas as pd
from sklearn.tree import DecisionTreeRegressor

data = pd.read_csv("tariff_data.csv")

X = data[['power','duration','time']]
y = data['cost']

model = DecisionTreeRegressor()
model.fit(X,y)

def predict_cost(power,duration,time):
    prediction = model.predict([[power,duration,time]])
    return round(prediction[0],2)