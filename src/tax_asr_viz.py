import numpy as np
import json
import folium
import h3
import branca.colormap as cm
from geojson.feature import Feature, FeatureCollection

def counts_by_hexagon(plot_variable, df, resolution):
    """
    Use h3.geo_to_h3 to index each data point into the spatial index of the specified resolution.
    Use h3.h3_to_geo_boundary to obtain the geometries of these hexagons
    
    Ex counts_by_hexagon(data, 9)
    """
    df = df[["lat","lng",plot_variable]]
    
    df["hex_id"] = df.apply(lambda row: h3.geo_to_h3(row["lat"], row["lng"], resolution), axis = 1)
    
    df_aggreg = df.groupby(by = "hex_id").size().reset_index()
#     print(df_aggreg.columns)
#     import numpy as np
    df_aggreg=df.groupby(['hex_id'], as_index=True).agg({plot_variable: 'mean' } ).rename(columns={plot_variable: 'value'}).reset_index()
    df_aggreg=df_aggreg[['hex_id', 'value']]
    df_aggreg=df_aggreg[df_aggreg['value']!=np.inf]
    
    df_aggreg["geometry"] =  df_aggreg.hex_id.apply(lambda x: 
                                                           {    "type" : "Polygon",
                                                                 "coordinates": 
                                                                [h3.h3_to_geo_boundary(h=x,geo_json=True)]
                                                            }
                                                        )
    
    return df_aggreg

def choropleth_map(df_aggreg, border_color = 'black', fill_opacity = 0.7, initial_map = None, with_legend = False,
                   kind = "linear"):
    
    """
    Creates choropleth maps given the aggregated data.
    """    
    #colormap
    min_value = df_aggreg["value"].min()
    max_value = df_aggreg["value"].max()
    m = round ((min_value + max_value ) / 2 , 0)
    
    #take resolution from the first row
    res = h3.h3_get_resolution(df_aggreg.loc[1,'hex_id'])
    
    if initial_map is None:
        f = folium.Figure(width=1000, height=1000)
        initial_map = folium.Map(location= [40.7128, -74.0060], zoom_start=10, tiles="cartodbpositron", 
                attr= '© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="http://cartodb.com/attributions#basemaps">CartoDB</a>' 
            ).add_to(f)
        

    #the colormap 
    #color names accepted https://github.com/python-visualization/branca/blob/master/branca/_cnames.json
    if kind == "linear":
        custom_cm = cm.LinearColormap(['green','yellow','red'], vmin=min_value, vmax=max_value)
    elif kind == "outlier":
        #for outliers, values would be -11,0,1
        custom_cm = cm.LinearColormap(['blue','white','red'], vmin=min_value, vmax=max_value)
    elif kind == "filled_nulls":
        custom_cm = cm.LinearColormap(['sienna','green','yellow','red'], 
                                      index=[0,min_value,m,max_value],vmin=min_value,vmax=max_value)
   

    #create geojson data from dataframe
    geojson_data = hexagons_dataframe_to_geojson(df_hex = df_aggreg)
    
    #plot on map
    name_layer = "Choropleth " + str(res)
    if kind != "linear":
        name_layer = name_layer + kind
        
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': custom_cm(feature['properties']['value']),
            'color': border_color,
            'weight': 1,
            'fillOpacity': fill_opacity 
        }, 
        name = name_layer
    ).add_to(initial_map)
    #add legend (not recommended if multiple layers)
    if with_legend == True:
        custom_cm.add_to(initial_map)
    return initial_map

def hexagons_dataframe_to_geojson(df_hex, file_output = None):
    """
    Produce the GeoJSON for a dataframe that has a geometry column in geojson 
    format already, along with the columns hex_id and value
    
    Ex counts_by_hexagon(data)
    """    
    list_features = []
    
    for i,row in df_hex.iterrows():
        feature = Feature(geometry = row["geometry"] , id=row["hex_id"], properties = {"value" : row["value"]})
        list_features.append(feature)
        
    feat_collection = FeatureCollection(list_features)
    
    geojson_result = json.dumps(feat_collection)
    
    #optionally write to file
    if file_output is not None:
        with open(file_output,"w") as f:
            json.dump(feat_collection,f)
    
    return geojson_result



# def plot_scatter(df, metric_col, x='lng', y='lat', marker='.', alpha=1, figsize=(16,12), colormap='viridis'):
#     """
#     Scatter plot function for h3 indexed objects
#     """    
#     df.plot.scatter(x=x, y=y, c=metric_col, title=metric_col
#                     , edgecolors='none', colormap=colormap, marker=marker, alpha=alpha, figsize=figsize);
#     plt.xticks([], []); plt.yticks([], [])

def create_hex_map(df_grouped_tax, plot_variable):
    
    df_tax_plot=df_grouped_tax[['lat','lng', plot_variable]]
    df_aggreg = counts_by_hexagon(plot_variable, df = df_tax_plot, resolution = 8)
    hexmap = choropleth_map(df_aggreg = df_aggreg, with_legend = False)
    hexmap.save(outfile = 'html/itax_map.html')
    return hexmap
