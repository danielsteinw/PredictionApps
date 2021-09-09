import pandas as pd
import numpy as np
import requests
import json
import streamlit as st
from sklearn import linear_model
from geopy.geocoders import Nominatim

if 'volume' not in st.session_state:
    st.session_state.volume = 0
if 'weight' not in st.session_state:
    st.session_state.weight = 0
if 'products_text' not in st.session_state:
    st.session_state.products_text = list()

#Get the Data from the Github csv
df = pd.read_csv('https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/transportCosts.csv')
df_dimensions = pd.read_csv('https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/dimensions.csv', index_col=0)
names_list = pd.read_csv('https://raw.githubusercontent.com/danielsteinw/PredictionApps/main/dimensions.csv')['Product'].to_list()

#Write the Header
st.write("""
# Transport Cost Prediction
This application predicts the **Transport Costs** for 4activeSystems GmbH.
""")

#Writhe the Header of the Sidebar
st.sidebar.header('User Input Parameters')

def calculate_coords_destination(destination):
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(destination)
    return loc

def calculate_coords_start(country, city):
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(city + ',' + country)
    return loc

def formate_dimensions(product):

    text = product + ": " + str(df_dimensions.loc[product, 'Length [cm]']) + 'x' + str(df_dimensions.loc[product, 'Width [cm]']) \
    + 'x' + str(df_dimensions.loc[product, 'Height [cm]']) + 'cm³, ' \
    + str(df_dimensions.loc[product, 'Weight [kg]']) + 'kg'
    return text


def user_input_features():

    express = st.sidebar.checkbox('Express Shipment')
    hazardous = st.sidebar.checkbox('Hazardous Goods')
    st.sidebar.subheader('Destination')
    destination = st.sidebar.text_input('City, Country')
    coords_start = calculate_coords_start("Austria", "Traboch")
    if destination=="":
        destination="Traboch, Austria"
    coords_destination = calculate_coords_destination(destination)
    if coords_destination is None:
        coords_destination = coords_start

    datamap = np.array([(coords_destination.latitude, coords_destination.longitude)])
    df_map = pd.DataFrame(datamap, columns=['lat', 'lon'])

    #Berechnen der Distanz
    r = requests.get(
        f"http://router.project-osrm.org/route/v1/car/{coords_start.longitude},{coords_start.latitude};{coords_destination.longitude},{coords_destination.latitude}?overview=false""")
    routes = json.loads(r.content)
    route_1 = routes.get("routes")[0]
    route_1.get('distance')
    distance = round(route_1.get('distance')/1000)

    show_distance_manually = st.sidebar.checkbox('Enter Distance manually')
    if show_distance_manually:
        distance = st.sidebar.slider('Distance [km]', 1, 3000)
        st.sidebar.write('Distance: ' + str(distance) + 'km')
    else:
        st.sidebar.write('Distance: ' + str(round(route_1.get('distance') / 1000)) + 'km')

    st.sidebar.write("""
    ### Products for Shipment
        """)

    products_radio = st.sidebar.radio('Products', names_list)

    st.sidebar.write(formate_dimensions(products_radio))
    products_add = st.sidebar.button('Add Product')

    if products_add:
            st.session_state.products_text.append(formate_dimensions(products_radio))
            st.session_state.volume += df_dimensions.loc[products_radio, 'Length [cm]'] \
            * df_dimensions.loc[products_radio, 'Width [cm]'] * df_dimensions.loc[products_radio, 'Height [cm]']
            st.session_state.weight += df_dimensions.loc[products_radio, 'Weight [kg]']

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
        st.session_state.products_text.append(str('Extra Package: ') + str(package_length) + str('x') + str(package_width) +
                                              str('x') + str(package_height) + str('cm³, ') + str(package_weight) + '.0' + 'kg')

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

    return features, df_map


dftwo, df_map = user_input_features()
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
st.map(df_map)
st.write('___________________________________________________________________________')
show_data = st.checkbox('Show Packing Dimensions')

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

#________________________________________________________________________________________


