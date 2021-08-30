import pandas as pd
import streamlit as st
from sklearn import linear_model

if 'volume' not in st.session_state:
    st.session_state.volume = 0
if 'weight' not in st.session_state:
    st.session_state.weight = 0
if 'products_text' not in st.session_state:
    st.session_state.products_text = list()

#Get the Data from the Github csv
df = pd.read_csv('https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/transportCosts.csv')
df_dimensions = pd.read_csv('https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/dimensions.csv')

#Write the Header
st.write("""
# Transport Cost Prediction
This application predicts the **Transport Costs** for 4activeSystems GmbH.
""")

#Writhe the Header of the Sidebar
st.sidebar.header('User Input Parameters')

def user_input_features():

    express = st.sidebar.checkbox('Express Shipment')
    hazardous = st.sidebar.checkbox('Hazardous Goods')
    distance = st.sidebar.slider('Distance [km]', 1, 3000)

    st.sidebar.write("""
    ### Products for Shipment
        """)

    products_opt = ['FB large', 'FB small', 'SB', 'XB', 'PA', 'PA child', 'PS', 'PS child', 'BS', 'BS child', 'C2',
                    'MC', 'MC E-Scooter', 'EQ', 'FlexPli', 'AN static roe', 'AN static white tail deer',
                    'AN static wild boar', 'AN static moose']
    products_radio = st.sidebar.radio('Products', products_opt)
    products_add = st.sidebar.button('Add Product')

    if products_add:
        if products_radio == 'FB large':
            st.session_state.products_text.append(str('FB large'))
            st.session_state.volume += 3215360
            st.session_state.weight += 365
        if products_radio == 'FB small':
            st.session_state.products_text.append(str('FB small'))
            st.session_state.volume += 1443200
            st.session_state.weight += 240
        if products_radio == 'SB':
            st.session_state.products_text.append(str('SB'))
            st.session_state.volume += 1488000
            st.session_state.weight += 343
        if products_radio == 'XB':
            st.session_state.products_text.append(str('XB'))
            st.session_state.volume += 1768000
            st.session_state.weight += 650
        if products_radio == 'PA':
            st.session_state.products_text.append(str('PA'))
            st.session_state.volume += 380000
            st.session_state.weight += 10
        if products_radio == 'PA child':
            st.session_state.products_text.append(str('PA child'))
            st.session_state.volume += 144000
            st.session_state.weight += 5
        if products_radio == 'PS':
            st.session_state.products_text.append(str('PS'))
            st.session_state.volume += 380000
            st.session_state.weight += 7
        if products_radio == 'PS child':
            st.session_state.products_text.append(str('PS child'))
            st.session_state.volume += 144000
            st.session_state.weight += 4
        if products_radio == 'BS':
            st.session_state.products_text.append(str('BS'))
            st.session_state.volume += 360000
            st.session_state.weight += 15
        if products_radio == 'BS child':
            st.session_state.products_text.append(str('BS child'))
            st.session_state.volume += 240000
            st.session_state.weight += 11
        if products_radio == 'C2':
            st.session_state.products_text.append(str('C2'))
            st.session_state.volume += 4099536
            st.session_state.weight += 163
        if products_radio == 'MC':
            st.session_state.products_text.append(str('MC'))
            st.session_state.volume += 1376172
            st.session_state.weight += 40
        if products_radio == 'MC E-Scooter':
            st.session_state.products_text.append(str('MC E-Scooter'))
            st.session_state.volume += 1376172
            st.session_state.weight += 45
        if products_radio == 'EQ':
            st.session_state.products_text.append(str('EQ'))
            st.session_state.volume += 3208500
            st.session_state.weight += 391
        if products_radio == 'FlexPli':
            st.session_state.products_text.append(str('FlexPli'))
            st.session_state.volume += 700
            st.session_state.weight += 1
        if products_radio == 'AN static roe':
            st.session_state.products_text.append(str('AN static roe'))
            st.session_state.volume += 275000
            st.session_state.weight += 5
        if products_radio == 'AN static white tail deer':
            st.session_state.products_text.append(str('AN static white tail deer'))
            st.session_state.volume += 1365336
            st.session_state.weight += 28
        if products_radio == 'AN static wild boar':
            st.session_state.products_text.append(str('AN static wild boar'))
            st.session_state.volume += 1224468
            st.session_state.weight += 23
        if products_radio == 'AN static moose':
            st.session_state.products_text.append(str('AN static moose'))
            st.session_state.volume += 6075000
            st.session_state.weight += 100


    st.sidebar.write("""
    ### Further Packages
        """)

    package_length = st.sidebar.number_input(label = 'Length [cm]', step=1)
    package_width = st.sidebar.number_input(label='Width [cm]', step=1)
    package_height = st.sidebar.number_input(label='Height [cm]', step=1)
    package_weight = st.sidebar.number_input(label = 'Weight [kg]', step=1)

    if st.sidebar.button('Add Package'):
        st.session_state.volume += package_length*package_width*package_height
        st.session_state.weight += package_weight
        st.session_state.products_text.append(str('Package: ') + str(package_length) + str('x') + str(package_width) +
                                              str('x') + str(package_height) + str('cm³, ') + str(package_weight) + 'kg')

    st.sidebar.write(str('__________________________________'))

    if st.sidebar.button('Remove all Packages'):
        st.session_state.volume = 0
        st.session_state.weight = 0
        st.session_state.products_text = []

    data = {'Express': express,
            'Hazardous': hazardous,
            'Distance': distance,
            'Volume': st.session_state.volume,
            'Weight': st.session_state.weight}
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

st.subheader('Considered Products and Packages')
if not st.session_state.products_text:
    st.write('Nothing has been added to the calculation yet.')
else:
    st.write(st.session_state.products_text)

st.subheader('Result')
float_formatter = "{:.2f}".format

if predicted_costs[0] > 0:
    if st.session_state.products_text:
        st.write(float_formatter(predicted_costs[0]) + ' €')
    else:
        st.write('Due to the input parameters no costs could be calculated.')
else:
    st.write('Due to the input parameters no costs could be calculated.')


st.subheader('Quality Measure of the Result')
st.write('R² = ' + float_formatter(regr.score(X, y)*100) + '%')

st.write('___________________________________________________________________________')
show_data = st.checkbox('Show Data')

if show_data:
    st.write(df_dimensions.style.format({'Weight [kg]': lambda x : '{:.0f}'.format(x)}))

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

