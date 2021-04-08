#Load the packages
import pandas as pd
import numpy as np
import pickle
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

#scikit learn libraries
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn import base


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

class DictEncoder(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col):
        self.col = col
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        def to_dict(l):
            try:
                return {x: 1 for x in l}
            except TypeError:
                return {}
        
        return X[self.col].apply(to_dict)

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

#####  USER Survey form 
@app.route('/user_form', methods =['GET'])
def user_form():

    if request.method == 'POST':
        rental_space_type = request.form['rental_space_type']
        rental_space_min  = request.form['rental_space_min']
        rental_space_max  = request.form['rental_space_max']

        keyfeature1  = request.form['keyfeature1']
        keyfeature2  = request.form['keyfeature2']
        keyfeature3  = request.form['keyfeature3']
        keyfeature4  = request.form['keyfeature4']
        keyfeature5  = request.form['keyfeature5']

        if rental_space_type == None:
            rental_space_type = 'RETAIL'
        if rental_space_min == None:
            rental_space_min = 100
        if rental_space_max == None:
            rental_space_max = 100000
    # if request.args.get("rental_space_type") == None:
    #     rental_space_type = 'RETAIL'
    # else:        
    #     rental_space_type = request.args.get("rental_space_type").strip()

    
    # if request.args.get("rental_space_min") == None:
    #     rental_space_min = 100
    # else:        
    #     rental_space_min = int(request.args.get("rental_space_min").strip())
    
    # if request.args.get("rental_space_max") == None:
    #     rental_space_max = 10000
    # else:        
    #     rental_space_max = int(request.args.get("rental_space_max").strip())

    # keyfeature1 = request.args.get("keyfeature1")
    # keyfeature2 = request.args.get("keyfeature2")
    # keyfeature3 = request.args.get("keyfeature3")
    # keyfeature4 = request.args.get("keyfeature4")
    # keyfeature5 = request.args.get("keyfeature5")

    return render_template('user_form.html')

@app.route('/recomm_eng', methods =['GET', 'POST'])
def recomm_eng():

    
    if request.method == "POST":
        
        rental_space_type = request.form['place_type']
        rental_space_min  = float(request.form['rental_space_min'])
        rental_space_max  = float(request.form['rental_space_max'])

        keyfeature1  = request.form['keyfeature1']
        keyfeature2  = request.form['keyfeature2']
        keyfeature3  = request.form['keyfeature3']
        keyfeature4  = request.form['keyfeature4']
        keyfeature5  = request.form['keyfeature5']

    if rental_space_type == None:
        rental_space_type = 'RETAIL'
    if rental_space_min == None:
        rental_space_min = 100
    if rental_space_max == None:
        rental_space_max = 100000
    
    # Read processed data frame and features files
    df_prop_ny_poi=pd.read_csv('data/properties_geolocation_ny_mean_radius.csv')
    feat_pipe = pickle.load( open("data/feat_pipe.p", "rb" ) )
    features = pickle.load( open("data/features.p", "rb" ) )

    # User form to data frame for prediction
    key_feature_list=[keyfeature1,keyfeature2,keyfeature3,keyfeature4,keyfeature5]
    temp_feat_list=[]
    for item in key_feature_list:
        if item not in temp_feat_list:
            if item: 
                temp_feat_list.append(item)
    key_feature_list=temp_feat_list
    # Make unique list of required features
    user_entry_list=[]
    for item in list(df_prop_ny_poi.columns):
        if item == 'features_fmt':
            user_entry_list.append(key_feature_list)
        else:
            user_entry_list.append(None)
    df_user_entry=pd.DataFrame([user_entry_list],columns=list(df_prop_ny_poi.columns))

    user_entry_features = feat_pipe.transform(df_user_entry)


    # Nearest Neighbors for the required features in data frame df
    nn = NearestNeighbors(n_neighbors=20).fit(features)
    dists, indices = nn.kneighbors(user_entry_features)
    df=df_prop_ny_poi.iloc[indices[0]]
    df['feat_dist'] = dists[0]

    ## Slack for the constraints on the max leasing space . Default is 5 %.
    space_slack=0.05
    min_space=rental_space_min - space_slack * rental_space_min 
    max_space=rental_space_max + space_slack * rental_space_max 

    # Drop the unneccessary columns and filter out the spaces which are outside of the square footage criteria
    mask=(df.leasable_square_foot >= min_space) & (df.leasable_square_foot <= max_space) 
    col_select=['address_id','leasable_square_foot','description','features_fmt','slug', 'feat_dist'] + [rental_space_type+'_plus_mean_rad', rental_space_type+'_minus_mean_rad']
    df=df[mask][col_select]
    df.rename(columns={rental_space_type+'_plus_mean_rad' :'plus_mean_rad', rental_space_type+'_minus_mean_rad' :'minus_mean_rad'}, inplace=True)

    # Replace nan values with more than the max values
    df['plus_mean_rad'].fillna(df['plus_mean_rad'].max()+2, inplace=True)
    df['minus_mean_rad'].fillna(df['minus_mean_rad'].max()+2, inplace=True)

    # scale the feature distances and the mean radius for poi data
    scaler = MinMaxScaler(feature_range=(0,1))
    df['scaled_feat_dist'] = scaler.fit_transform(df['feat_dist'].to_frame())
    df['scaled_plus_mean_rad'] = scaler.fit_transform(df['plus_mean_rad'].to_frame())
    df['scaled_minus_mean_rad'] = scaler.fit_transform(df['minus_mean_rad'].to_frame())
    df['scaled_net_mean_rad'] = scaler.fit_transform((df['scaled_plus_mean_rad'] - df['scaled_minus_mean_rad']).to_frame())

    # Weigh the feature data score and the poi score
    feat_wt = 1 
    poi_wt  = 1
    df['suitability_score']=( feat_wt * df['scaled_feat_dist']  + poi_wt * df['scaled_net_mean_rad'])/(feat_wt + poi_wt) 
    df['suitability_score']=df['suitability_score'].round(3)

    # Drop the unncessary columns for score computation
    drop_list=['feat_dist','plus_mean_rad','minus_mean_rad','scaled_feat_dist','scaled_plus_mean_rad','scaled_minus_mean_rad','scaled_net_mean_rad']
    df.drop(columns=drop_list,inplace=True)

    # Rank the properties as per suitability score
    df.sort_values(by=['suitability_score'], ascending=False, inplace=True)

    # Convert data frame to tuple format
    records = df.to_records(index=False)
    data = list(records)
    # data=[(1,2,3), (1,2,3), (3,5,44)]

    # Columns displayed are below
    # print_col_list=
    # ['address_id',
    # 'leasable_square_foot',
    # 'description',
    # 'features_fmt',
    # 'slug',
    # 'suitability_score']

    return render_template('recommendation.html', data = data)

#####
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    # app.run(port=8000, debug=True)
    app.run(debug=False)