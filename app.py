#Load the packages
import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import folium

import requests
#Bokeh imports
# from bokeh.models import Select, TextInput
from bokeh.models import Div
# from bokeh.layouts import column, row
from bokeh.embed import components

#src imports
from src.demo_viz import create_map
from src.tax_asr_viz import create_hex_map
from src.poi_viz import select_df_and_map

demo_menu_list=['median_employee_salary',
        'population_density',
        'per_capita_income',                     
        'total_population_count',
        'expenses_apparel',
        'expenses_contributions',
        'expenses_education',
        'expenses_entertainment',
        'expenses_food_beverage',
        'expenses_gifts',
        'expenses_healthcare',
        'expenses_home_furnishings',
        'expenses_household_operations',
        'expenses_misc_expenses',
        'expenses_personal_care',
        'expenses_personal_insurance',
        'expenses_reading',
        'expenses_shelter',
        'expenses_tabacco',
        'expenses_transportation',
        'expenses_utilities']

tax_assessor_list=['assessed_value_total', 'assessed_value_land', 'last_sale_amount']

poi_list=['RETAIL', 'RESTAURANT', 'FITNESS', 'BEAUTY', 'BANK', 'PHARMACY', 'MEDICAL', 'BAR-CAFE']

app = Flask(__name__)



@app.route('/')
def index():

    #Render the page
    return render_template('index.html')

@app.route('/demographics', methods = ['GET', 'POST'])
def demographics():
    
    df_demo_join_cherre=pd.read_csv('data/demo_data.csv')
    df_demo_join_cherre['zip']=df_demo_join_cherre['zip'].astype(str)
    if request.method == 'GET':
        demo_name = request.args.get("demo_name")
    if demo_name is None:
        demo_name = demo_menu_list[0]

    
    # select = Select(title='Demographic attribute', value='median_employee_salary', options=menu_list, width =500)
    div=Div(text="<iframe src="r'html/imap.html'" style='min-width:calc(100vw - 26px); height: 500px'><iframe>", width=500)

    attribute= demo_name

    demog_m=create_map(df_demo_join_cherre, 'zip', attribute, 'per Zipcode')

    div.text=demog_m._repr_html_()

    demo_script, demo_div = components(div)
    
    return render_template('demographics.html', script=demo_script, div=demo_div, demo_name=demo_name, demo_attributes=demo_menu_list)

@app.route('/property_info', methods =['GET', 'POST'])
def property_info():

    df_group_tax=pd.read_csv('data/tax_df.csv')
    
    if request.method == 'GET':
        tax_asr_name = request.args.get("tax_asr_name")

    if tax_asr_name is None:
        tax_asr_name = tax_assessor_list[0]
    
    
    # select = Select(title='property assessment attribute', value='assessed_value_total', options=tax_assessor_list, width =500)
    div=Div(text="<iframe src="r'html/itax_map.html'" style='min-width:calc(100vw - 26px); height: 500px'><iframe>", width=500)

    plot_variable = tax_asr_name
    tax_attr_m=create_hex_map(df_group_tax, plot_variable)
    div.text=tax_attr_m._repr_html_()

    tax_asr_script, tax_asr_div = components(div)    

    return render_template('tax_asr.html', script=tax_asr_script, div=tax_asr_div, tax_asr_name=tax_asr_name, tax_asr_attributes=tax_assessor_list)

@app.route('/places_of_interest', methods =['GET', 'POST'])
def places_of_interest():

    df=pd.read_csv('data/poi_data_NY.csv')
    
    if request.method == 'GET':
        place_type_name = request.args.get("poi_type_name", 'RETAIL')
        if request.args.get("poi_rad") == None:
            place_radius = 2.0
        else:        
            place_radius = float(request.args.get("poi_rad").strip())
            
        if request.args.get("center_lat") == None:
            center_latitude = 40.753912
        else:
            center_latitude = float(request.args.get("center_lat", 40.753912).strip())
        if request.args.get("center_long") == None:
            center_longitude=-73.981205
        else:
            center_longitude = float(request.args.get("center_long", -73.981205).strip())

    # select = Select(title="Type of rental space", value="RETAIL", options=poi_options_list)
    # radius = TextInput(title="Radius of places to check in km", value="5.0")
    # center_latitude = TextInput(title="Enter the latitude as float", value="40.753912")
    # center_longitude = TextInput(title="Enter the longitude as float", value="-73.981205")
    div=Div(text="<iframe src="r'html/i_poi_map.html'" style='min-width:calc(100vw - 26px); height: 500px'><iframe>", width=500)

    # place_type = select.value
    # place_radius=float(radius.value)
    # c_lat=float(center_latitude.value)
    # c_long=float(center_longitude.value)
    
    poi_map=select_df_and_map(df, place_type_name, place_radius, center_latitude, center_longitude)

    div.text=poi_map._repr_html_()

    poi_script, poi_div = components(div)

    return render_template('poi.html', script=poi_script, div=poi_div, poi_type_name=place_type_name, poi_rad =place_radius, center_lat = center_latitude, center_long=center_longitude, place_type_list=poi_list)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
    # app.run(debug=False)