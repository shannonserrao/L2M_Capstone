import json
import folium

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

# table = main table/data frame we read from (pandas DataFrame)
# zips = column name where ZIP codes are (string)
# mapped_feature = column name for feature we want to visualize (string)
# add_text = any additional commentary to be added in the map legend (string)

def create_map(table, zips, mapped_feature, add_text = ''):
    # reading of the updated GeoJSON file
    nyc_geo = r'data/nyc_updated-file.json'
    # initiating a Folium map with NYC's longitude and latitude 40.7128° N, 74.0060° W
    f = folium.Figure(width=1000, height=1000)
    m = folium.Map(location = [40.7128, -74.0060], zoom_start = 10, width=500, height=500).add_to(f)
    # creating a choropleth map
    m.choropleth(
        geo_data = nyc_geo,
        fill_color = 'YlGn',
        fill_opacity = 0.6,
        line_opacity = 0.8,
        data = table,
        # refers to which key within the GeoJSON to map the ZIP code to
        key_on = 'feature.properties.zcta',
        # first element contains location information, second element contains feature of interest
        columns = [zips, mapped_feature],
        legend_name = (' ').join(mapped_feature.split('_')).title() + ' ' + add_text + ' Across NYC'
    )
    folium.LayerControl().add_to(m)
    print(mapped_feature)
    # save map with filename based on the feature of interest
#     m.save(outfile = mapped_feature + '_map.html')
    m.save(outfile = 'html/imap.html')
    return m



# def modify_doc(doc):

    
#     select = Select(title='Demographic attribute', value='median_employee_salary', options=menu_list, width =500)
#     div=Div(text="<iframe src="r'imap.html'" style='min-width:calc(100vw - 26px); height: 500px'><iframe>", width=500)

#     def update_attribute(attrname, old, new):
#         attribute = select.value
#         demog_m=create_map(df_demo_join_cherre, 'zip', attribute, 'per Zipcode')

#         div.text=demog_m._repr_html_()

#         return div
        
#     select.on_change('value', update_attribute)
    
#     layout = column(row(select), row(div))

#     doc.add_root(layout)

# # show(modify_doc, notebook_url="localhost:8890")