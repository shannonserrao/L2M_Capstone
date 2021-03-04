#Load the packages
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

#Bokeh imports

# from bokeh.server.server import Server

# from bokeh.models import HoverTool, ColumnDataSource, CustomJS
# #from bokeh.charts import Scatter
# from bokeh.palettes import Spectral9
# from bokeh.plotting import figure, show

# from os.path import dirname, join

# # Bokeh basics 
# from bokeh.io import curdoc
# # from bokeh.models.widgets import Tabs
# # from bokeh.plotting import curdoc
# from bokeh.palettes import Category20_8
# from bokeh.embed import components, server_document
# from scripts.histogram import histogram_tab
# from scripts.timeplot import timeplot_tab


app = Flask(__name__)

# input_data = pd.read_csv('./data/timeplot.csv')


# def make_dataset(grouplabels, lstlabels, feature_to_plot, rw_colors):

#     # Dataframe to hold information
#     # groupaddr[groupaddr['label']!='white']['count'].plot.hist(bins=number_bins, alpha=0.5)
#     # by_rware=[]
#     xs = []
#     ys = []
#     colors = []
#     labels = []
#     # if feature_to_plot==None:
#     #     feature_to_plot='count'
#     # print('make data set feature' + str(feature_to_plot))

#     for i, label in enumerate(lstlabels):
#         subset=grouplabels[grouplabels['label']==label].sort_values(by=['date'])
#         print('label selected is ' + str(label))
#         # Evenly space x values
#         x = subset['date']
#         # Evaluate pdf at every value of x
#         y = subset[subset['label']==label][feature_to_plot]
#         # print(y)
#         # print(x)
#         # Append the values to plot
#         xs.append(list(x))
#         ys.append(list(y))
#         # Append the colors and label
#         colors.append(rw_colors[i])
#         labels.append(label)
#         # print(type(ys))

#     new_src = ColumnDataSource(data={'x': xs, 'y': ys, 
#                                 'color': colors, 'label': labels})
#     return new_src

# def style(p):
#     # Title 
#     p.title.align = 'center'
#     p.title.text_font_size = '20pt'
#     p.title.text_font = 'serif'
#     # Axis titles
#     p.xaxis.axis_label_text_font_size = '14pt'
#     p.xaxis.axis_label_text_font_style = 'bold'
#     p.yaxis.axis_label_text_font_size = '14pt'
#     p.yaxis.axis_label_text_font_style = 'bold'
#     # Tick labels
#     p.xaxis.major_label_text_font_size = '12pt'
#     p.yaxis.major_label_text_font_size = '12pt'

#     return p

# def make_plot(src,feature_to_plot):
#     # if feature_to_plot==None:
#     #     feature_to_plot='count'
#     # print('make plot feature' + str(feature_to_plot))
#     # plot_width = 1000, plot_height = 350,
#     p = figure(plot_width = 1300, plot_height = 650,
#                 title = 'time series of Ransom ware',
#                 x_axis_label = 'date', y_axis_label = 'Mean of ransomware %s ' % (feature_to_plot), x_axis_type="datetime")
    
#     p.multi_line('x', 'y', color = 'color', legend= 'label', 
#                     line_width = 3,
#                     source = src)
#     print('make plot')                
#     # Hover tool with next line policy
#     # hover = HoverTool(tooltips=[('ransomware', '@label'), 
#     #                             ('Date', '$x'),
#     #                             ('Ransomware family', '$y')],
#     #                     line_policy = 'next')
#     # # Add the hover tool and styling
#     # p.add_tools(hover)
#     # # p = style(p)
#     return p


#Connect the app


@app.route('/')
def index():

    # rw_colors = Category20_8
    # current_feature_select = request.args.get("feature_name")
    # if current_feature_select == None:
    #     current_feature_select = 'count'
    
    # feature_to_plot=current_feature_select

    # # print('Hello world')
    # src = make_dataset(grouplabels, lstlabels[1:], current_feature_select, rw_colors)
    # p = make_plot(src, current_feature_select)
    # script, div = components(p)
    # script, div = None
    #Render the page
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)