import pandas as pd
import streamlit as st
from sklearn import linear_model

#Get the Data from the Github csv
df = pd.read_csv('https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/transportCosts.csv')

#Write the Header
st.write("""
# Transport Cost Prediction
This application predicts the **Transport Costs** for 4activeSystems GmbH.
""")

#Writhe the Header of the Sidebar
st.sidebar.header('User Input Parameters')

st.sidebar.write("""
### Products for Shipment
    """)

def user_input_features():

    volume = 0
    weight = 0
    #FB large
    fb_large = st.sidebar.number_input(label = 'FB large', min_value = 0, step = 1)
    if fb_large > 0:
        volume += 3215360*fb_large
        weight += 365*fb_large
    #FB small
    fb_small = st.sidebar.number_input(label = 'FB small', min_value = 0, step = 1)
    if fb_small > 0:
        volume += 1443200*fb_small
        weight += 240*fb_small
    #SB
    sb = st.sidebar.number_input(label = 'SB', min_value = 0, step = 1)
    if sb > 0:
        volume += 1488000*sb
        weight += 343*sb

    st.sidebar.write("""
    ### Further Input Parameters
        """)

    express = st.sidebar.checkbox('Express Shipment')
    hazardous = st.sidebar.checkbox('Hazardous Goods')
    distance = st.sidebar.slider('Distance [km]', 1, 3000)
    extra_volume = st.sidebar.number_input(label = 'Extra Volume [cm³]', step=100)
    extra_weight = st.sidebar.number_input(label = 'Extra Weight [kg]', step=1)

    data = {'Express': express,
            'Hazardous': hazardous,
            'Distance': distance,
            'Volume': extra_volume+volume,
            'Weight': extra_weight+weight}
    features = pd.DataFrame(data, index=[0])
    return features


dftwo = user_input_features()
s = dftwo.style.format({'Volume': lambda x : '{:.0f}'.format(x), 'Weight': lambda y : '{:.0f}'.format(y)})

st.subheader('User Input Parameters')
st.write(s)

X = df[['Express', 'Hazardous', 'Distance', 'Volume', 'Weight']]
y = df['Costs']

regr = linear_model.LinearRegression()
regr.fit(X,y)

predicted_costs = regr.predict(dftwo)

st.subheader('Result')
float_formatter = "{:.2f}".format

if predicted_costs[0] > 0:
    st.write(float_formatter(predicted_costs[0]) + ' €')
else:
    st.write('Due to the input parameters no costs could be calculated.')


st.subheader('Quality Measure of the Result')
st.write('R² = ' + float_formatter(regr.score(X, y)*100) + '%')

#______________________________________________________________________________________

#https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/4a_Logo.svg

import base64
import requests

st.write("##")

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


url = "https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/4a_Logo.svg"
r = requests.get(url) # Get the webpage
svg = r.content.decode() # Decoded response content with the svg string

render_svg(svg) # Render the svg string
