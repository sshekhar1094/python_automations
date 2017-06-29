#!/usr/bin/python3.5

'''
    This file is a wrapper over bokeh.
    Provides one line functions for various kinds of plots
'''

# module imports
import pandas as pd
import numpy as np

# bokeh
from bokeh.plotting import figure
from bokeh.charts import Bar, Scatter, Donut, Histogram, BoxPlot
from bokeh.io import show
from bokeh.models.ranges import Range1d
from bokeh.models.sources import ColumnDataSource
from bokeh.models import HoverTool

# globals
ht = 100    # a unit for plot height, all will be multiples of this
colors = ['#f1595f', '#79c36a', '#599ad3', '#f9a65a', '#9e66ab', '#cd7058', '#d77fb3', '#727272']

# function to draw a bar graph
def bar_graph(Y, title='', ylabel='', xlabel='', x_labels=None, height=3):
    if(x_labels == None): x_labels = range(0, len(Y))

    dict = { 'values' : {} }
    i=0
    for i in range(0, len(Y)):
        dict['values'][x_labels[i]] = Y[i]
    df = pd.DataFrame(dict)
    df['label'] = df.index

    plot = Bar(df, values='values', label='label', bar_width=0.2, legend=None, title=title, plot_height=int(height*ht), sizing_mode='scale_width')
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel

    return plot


# function to draw horizontal bar graphs
def horizontal_bars(Y, title='', ylabel='', xlabel='', y_labels=None, height=3):
    data = {'Categories':{}}

    if(y_labels == None): y_labels = [''] * len(Y)

    i=0
    for i in range(0, len(Y)):
        data['Categories'][y_labels[i]] = Y[i]
    df_data = pd.DataFrame(data).sort(columns='Categories', ascending=False)
    this_series = df_data.loc[:, 'Categories']

    p = figure(height=int(height*ht), y_range=this_series.index.tolist(), sizing_mode='scale_width')
    p.grid.grid_line_alpha = 0.15
    p.grid.grid_line_color = "grey"
    p.xaxis.axis_label = xlabel
    p.yaxis.axis_label = ylabel

    j = 1
    for k, v in this_series.iteritems():
        p.rect(x=v / 2, y=j, width=abs(v), height=0.3, color='#F45666', width_units="data", height_units="data")
        j += 1


    return p


# function to draw line graphs
# Y has to be a list of lists, draws a line for each list in Y
def line_graph(Y, xlabel='', ylabel='', title='', legends=None, height=3, hover=None):
    if(legends == None): legends = [''] * len(Y)
    plot = figure(plot_height=int(height*ht), title=title, sizing_mode='scale_width')
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel
    i = 0
    for i in range(0, len(Y)):
        plot.line(y=Y[i], x=list(range(1, len(Y[i])+1)), legend=legends[i], line_width=3, color = colors[i % len(colors)])

    return plot



# function for scatter plot
def scatter_plot(X, Y, xlabel='', ylabel='', title='', height=3):
    dict = {'X':X, 'Y':Y}
    df = pd.DataFrame(dict)

    plot = Scatter(df, 'X', 'Y', title=title, plot_height=int(height*ht), sizing_mode='scale_width')
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel

    return plot



# function to draw pie charts
def pie_chart(Y, names, title='', height=3.8):
    print(Y, names)
    i = 0
    for i in range(0, len(Y)):
        names[i] = names[i] + ' = ' + str(Y[i])

    data = pd.Series(Y, index=names)
    pie = Donut(data, title=title, plot_height=int(height*ht), sizing_mode='scale_width')
    return pie


def bollinger_band(Y, upperband, lowerband, title='', xlabel='', ylabel='', height=3):
    X = range(0, len(Y))
    band_x = np.append(X, X[::-1])
    band_y = np.append(lowerband, upperband[::-1])
    plot = figure(title=title, plot_height = int(height*ht), sizing_mode='scale_width')
    plot.patch(band_x, band_y, color='#7570B3', fill_alpha=0.2)
    plot.line(X, Y, line_width=2)
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel

    return plot 


def histograms(Y, bins=50, title = '', xlabel='', height=3):
    df = { xlabel : Y}
    df = pd.DataFrame(df)
    plot = Histogram(df, xlabel, legend=None, bins=bins, title=title, plot_height=int(height*ht), sizing_mode='scale_width')
    return plot


def boxplot(Y, title='', xlabel='', ylabel='', height=6):
    df = {ylabel : Y}
    df = pd.DataFrame(df)
    df['label'] = xlabel
    plot = BoxPlot(df, values=ylabel, title=title, label='label', legend=None, color='#00cccc', plot_height=int(height*ht), sizing_mode='scale_width')
    return plot


# function to show how to draw line chart with hovering features, 
# def team_progress(Y, xlabel='', ylabel='', title='', height=3, concept=None, architecture=None, design=None, qa=None,
#                   sustenance=None, ce=None, team_compositions=None, cycle_times=None, values=None,
#                   priority=None, quality=None, ownership=None):
#     plot = figure(plot_height=int(height*ht), title=title, sizing_mode='scale_width')
#     plot.xaxis.axis_label = xlabel
#     plot.yaxis.axis_label = ylabel

#     source = ColumnDataSource(data = dict(
#         y = Y,
#         x = list(range(1, len(Y)+1)),
#         # multiplying by 100 to convert to percentage
#         concept = [str(int(c*100)) + '%' for c in concept],
#         architecture = [str(int(c*100)) + '%' for c in architecture],
#         design = [str(int(c*100)) + '%' for c in design],
#         qa = [str(int(c*100)) + '%' for c in qa],
#         sustenance = [str(int(c*100)) + '%' for c in sustenance],
#         ce = [str(int(c*100)) + '%' for c in ce],
#         priority = [str(int(p*100)) + '%' for p in priority],
#         quality=[str(int(p * 100)) + '%' for p in quality],
#         ownership=[str(int(p * 100)) + '%' for p in ownership],
#         compositions = team_compositions,
#         cycles = cycle_times,
#         values = values
#     ))
#     hover = HoverTool(tooltips=[
#                 ("Values", "@values"),
#                 ("Concept", "@concept"),
#                 ("Architecture", "@architecture"),
#                 ("Design", "@design"),
#                 ("Quality Assurance", "@qa"),
#                 ("Sustenance", "@sustenance"),
#                 ("Customer Engineering", "@ce"),
#                 ("Priority", "@priority"),
#                 ("Quality", "@quality"),
#                 ("Ownership", "@ownership"),
#                 ("Composition", "@compositions"),
#                 ("Cycle Time(days)", "@cycles")
#             ])

#     plot.line('x', 'y', source=source, line_width=3, color = 'red')
#     plot.add_tools(hover)
#     return plot
