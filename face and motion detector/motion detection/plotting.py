# import our dataframe from the motion dector file
from motion_detector import df
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import HoverTool, ColumnDataSource

#covert time to a string format
df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)


f=figure(x_axis_type='datetime', height=100, width=500, sizing_mode='scale_width', title="Time Graph")
f.yaxis.minor_tick_line_color=None
f.xaxis[0].ticker.desired_num_ticks = 20
# f.ygrid[0].ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
f.add_tools(hover)

p=f.quad(left="Start", right="End", bottom=0, top=1, color="red", source=cds) #source adds data soruce

output_file('Graph.html')
show(f)
