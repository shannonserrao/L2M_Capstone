import pandas as pd
import numpy as np
from math import pi
import folium
poi_options_list=['RETAIL', 'RESTAURANT', 'FITNESS', 'BEAUTY', 'BANK', 'PHARMACY', 'MEDICAL', 'BAR-CAFE']

def process_symbiotic_competition_business(df_poi, open_business, radius, c_lat, c_long):
    
    if open_business=='RETAIL':
        df_minus=retail_chk_fun(df_poi)
        df_plus=pd.concat([restaurants_chk_fun(df_poi), fitness_chk_fun(df_poi), beauty_chk_fun(df_poi), 
                          bank_chk_fun(df_poi),  pharmacy_chk_fun(df_poi), medical_chk_fun(df_poi),
                           bar_cafe_fun(df_poi)])
    elif open_business=='RESTAURANT':
        df_minus=restaurants_chk_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi) ,bank_chk_fun(df_poi), bar_cafe_fun(df_poi)])
    
    elif open_business=='FITNESS':
        df_minus=fitness_chk_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi),bank_chk_fun(df_poi),
                           pharmacy_chk_fun(df_poi), beauty_chk_fun(df_poi)])
    
    elif open_business=='BEAUTY':
        df_minus=beauty_chk_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi), bank_chk_fun(df_poi), fitness_chk_fun(df_poi),
                           pharmacy_chk_fun(df_poi)])
    
    elif open_business=='BANK':
        df_minus=bank_chk_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi),
                           restaurants_chk_fun(df_poi)])
        
    elif open_business=='PHARMACY':
        df_minus=pharmacy_chk_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi),
                           medical_chk_fun(df_poi) , bank_chk_fun(df_poi)])
    
    elif open_business=='MEDICAL':
        df_minus=medical_chk_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi),
                           pharmacy_chk_fun(df_poi) , bank_chk_fun(df_poi)])
    
    elif open_business=='BAR-CAFE':
        df_minus=bar_cafe_fun(df_poi)
        df_plus=pd.concat([retail_chk_fun(df_poi),
                           pharmacy_chk_fun(df_poi) , bank_chk_fun(df_poi), restaurants_chk_fun(df_poi)])
    else:
        column_names=list(df_poi.column_names)
                          
        df_plus=pd.DataFrame(columns = column_names)
        df_minus=pd.DataFrame(columns = column_names)
        
    df_plus=df_plus[distance_np(df_plus.latitude, df_plus.longitude, c_lat, c_long) <= radius]
    df_minus=df_minus[distance_np(df_minus.latitude, df_minus.longitude, c_lat, c_long) <= radius]
    
    return df_plus, df_minus

def distance_np(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 12742 * np.arcsin(np.sqrt(a)) #2*R*asin...

def retail_chk_fun(df, string='RETAIL'):
    ind_list=list(df['Industry'].unique())
    retail_check=check_type('retail', ind_list)+check_type('store', ind_list)
    return df[df.Industry.isin(retail_check)]

def restaurants_chk_fun(df, string='RESTAURANTS'):
    return df[df.line_of_business.isin(['RESTAURANTS'])]

def fitness_chk_fun(df, string='FITNESS'):
    ind_list=list(df['Industry'].unique())
    fitness_check=check_type('fitness', ind_list)+check_type('gym', ind_list)
    return df[(df.line_of_business.isin(['HEALTH CLUBS AND SPAS', 'SPORTS AND RECREATION'])) | (df.Industry.isin(fitness_check))]

def beauty_chk_fun(df, string='BEAUTY'):

    beauty_ind_list=['BEAUTY SALONS & DAY SPAS',
                     'BEAUTY SKIN CARE', 'BEAUTY SALONS', 'SPAS - BEAUTY AND DAY',
                     'SCHOOLS BEAUTY & BARBER',
                     'WIGS & HAIR PIECES', 'HAIR STYLISTS', 'HAIR SALONS & BARBERS', 'HAIR REMOVAL',
                     'HAIR WEAVING', 'BARBER`']
    return df[df.Industry.isin(beauty_ind_list)]

def bank_chk_fun(df, string='BANKS'):
    return df[df.category=='BANKS - FINANCIAL']

def pharmacy_chk_fun(df, string='PHARMACY'):
    return df[df.line_of_business=='PHARMACIES']

def medical_chk_fun(df, string='MEDICAL'):
    med_chk_list=['MEDICAL GROUPS', 'LABORATORIES MEDICAL', 
              'MEDICAL EQUIP & SUPPL', 'CLINICS MEDICAL', 
              'HOSPITALS, CLINICS & MEDICAL CENTERS', 'EMERGENCY MEDICAL AND SURGICAL', 
              'MEDICAL SVC ORGANIZATIONS', 'MEDICAL CENTERS', 'MEDICAL RESEARCH & DEVELOPMENT',
              'MEDICAL LABORATORIES', 'MEDICAL BILLING SVC', 
              'PHYS & SURGN SPORTS MEDICINE', 'ALTERNATIVE MEDICINE',
              'PHYS & SURGN INTERNAL MEDICINE', 'VETERINARY CLINICS & HOSPITALS',
              'HOSPITALS, CLINICS & MEDICAL CENTERS', 'HOSPITALS']
    return df[(df.Industry.isin(med_chk_list)) | (df.line_of_business.isin(['HOSPITALS']))]

def bar_cafe_fun(df, string='Bar-Cafe'):
    bar_list=['BARS - CLUBS',
           'BARS GRILLS & PUBS','BARS GRILLS & PUBS',
          'BREWERIES & BREW PUBS', 'CAFES', 'TAVERNS', 
          'BARS, TAVERNS & COCKTAIL LOUNGES', 'COCKTAIL LOUNGES', 
          'INNS']
    return df[df.Industry.isin(bar_list)]

def folium_pov_data(df_plus,df_minus, c_lat, c_long):
    
    f = folium.Figure(width=1000, height=1000)
    poi_map = folium.Map(location=[c_lat, c_long], zoom_start=16).add_to(f)
    
    folium.Marker(
        location=[c_lat, c_long],
        popup = (
                 'Reference Location: ' + '<br>'
                 'Latitude: '+ str(c_long) + '<br>'
                 'Longitude: ' + str(c_long) + '<br>'
                ),
        icon=folium.Icon(color="blue",icon="fa-map-pin", prefix='fa')
            ).add_to(poi_map)
    
    
    for lat, long, category, line_of_business, industry, zipcode in zip(df_plus['latitude'], df_plus['longitude'], df_plus['category'], df_plus['line_of_business'], df_plus['Industry'], df_plus['zip']):
        folium.Marker(
        location=[lat, long],
        popup = (
                 'Industry: ' + industry + '<br>'
                 'Line of business: ' + str(line_of_business)+'<br>'
                 'category: ' + str(category)+'<br>'
                 'Zipcode: ' + str(zipcode) + '<br>'
                ),
        icon=folium.Icon(color="green",icon="plus-circle", prefix='fa')
            ).add_to(poi_map)
    
    for lat, long, category, line_of_business, industry, zipcode in zip(df_minus['latitude'], df_minus['longitude'], df_minus['category'], df_minus['line_of_business'], df_minus['Industry'], df_minus['zip']):
        folium.Marker(
        location=[lat, long],
        popup = (
                 'Industry: ' + industry + '<br>'
                 'Line of business: ' + str(line_of_business)+'<br>'
                 'category: ' + str(category)+'<br>'
                 'Zipcode: ' + str(zipcode) + '<br>'
                ),
        icon=folium.Icon(color="red",icon="minus-circle", prefix='fa')
            ).add_to(poi_map)
    
    poi_map.save(outfile = 'html/i_poi_map.html')
    return poi_map

def select_df_and_map(df, place_type, place_radius, c_lat, c_long):
    df_plus, df_minus = process_symbiotic_competition_business(df, place_type, place_radius, c_lat, c_long)
    return folium_pov_data(df_plus, df_minus, c_lat, c_long)

def check_type(string,chk_list):
    op_list=[]
    for item in chk_list:
        if string in item.lower():
            op_list.append(item)
    return op_list
