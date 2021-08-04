import pandas as pd
import streamlit as st
import os
from pathlib import Path
from sklearn import linear_model

#Reading the csv

path = os.path.dirname(__file__)
my_file = path+'/transportCosts.csv'
df = pd.read_csv(my_file)

#Calculation
X = df[['Express','Hazardous','Distance','Volume','Weight']]
y = df['Costs']

regr = linear_model.LinearRegression()
regr.fit(X, y)

predictedCosts = regr.predict([[0,0,628.28,4074840,167.8]])

#App
st.write("""
# Transport Costs Prediction Application

This App predicts the transportation costs!
""")


