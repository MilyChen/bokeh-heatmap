'''
Created on Aug 27, 2017

@author: Mily
'''
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure

# source data from weatherstats.ca based on Environment and Climate Change Canada data
months_l = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
output_file("toronto_rain.html")

rain_data = pd.read_csv('C:\Users\Mily.mc-pc\Desktop\weather data.csv')
rain_data = rain_data.dropna()

data = pd.DataFrame()
data['Year'] = rain_data['date'].apply(lambda x: x.split("/")[2])  # isolate Years from date
data['Year'] = data['Year'].astype(str)
data['Month'] = rain_data['date'].apply(lambda x: x.split("/")[0])  # isolate month from date
data['Month'] = data['Month'].apply(lambda x: months_l[int(x) - 1])  # format months 
data["rain"] = rain_data['rain_v']

data= data.pivot(index='Year', columns = 'Month', values ='rain') #reshape the dataframe, Year as rows, month as cols
data.columns.name = 'Month'

data = data.reindex(columns=months_l) #resort columns by order of months list
df = pd.DataFrame(data.stack(), columns=['rain']).reset_index()

#print data
#print df

source = ColumnDataSource(df)  

colors = ["#ffffff","#e6f7ff","#b3e6ff","#80d4ff","#4dc3ff"," #1ab2ff","#0099e6","#0077b3","#005580","#00334d"]

mapper = LinearColorMapper(palette=colors, low=df.rain.min(), high=df.rain.max())

p = figure(title="Toronto Rainfall", x_range=list(data.index), y_range=list(reversed(data.columns))
                ,tools="")

p.rect('Year', 'Month', width=1, height=1, source=source, line_color=None, fill_color={'field': 'rain', 'transform':mapper}) 
       
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