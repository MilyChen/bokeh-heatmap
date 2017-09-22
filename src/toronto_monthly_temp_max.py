'''
Created on Aug 27, 2017

@author: Mily
'''
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.palettes import brewer

# source data from weatherstats.ca based on Environment and Climate Change Canada data
months_l = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
output_file("toronto_temp.html")

temp_data = pd.read_csv('C:\...\weather data.csv')
temp_data = temp_data.dropna()

data = pd.DataFrame()
data['Year'] = temp_data['date'].apply(lambda x: x.split("/")[2])  # isolate Years from date
data['Year'] = data['Year'].astype(str)
data['Month'] = temp_data['date'].apply(lambda x: x.split("/")[0])  # isolate month from date
data['Month'] = data['Month'].apply(lambda x: months_l[int(x) - 1])  # format months 
data["temp"] = temp_data['max_temperature_v']

data = data.pivot(index='Year', columns='Month', values='temp')  # reshape the dataframe, Year as rows, month as cols
data.columns.name = 'Month'

data = data.reindex(columns=months_l)  # resort columns by order of months list
df = pd.DataFrame(data.stack(), columns=['temp']).reset_index()

source = ColumnDataSource(df)  

colors = brewer['RdBu'][10]

mapper = LinearColorMapper(palette=colors, low=df.temp.min(), high=df.temp.max())

p = figure(title="Toronto Temperature (1938-2017)", x_range=list(data.index), y_range=list(reversed(data.columns))
                , tools="")

p.rect('Year', 'Month', width=1, height=1, source=source, line_color=None, fill_color={'field': 'temp', 'transform':mapper}) 
       
color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"))
p.add_layout(color_bar, 'right')

p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.0

show(p)
