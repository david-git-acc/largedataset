import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

redbluecmap = plt.get_cmap("seismic")

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

# Get sign of number. Didn't want to import entire maths module for it
def sgn(x):
    if x == 0:
        return 0
    return abs(x) / x

names = ["Heathrow" , "Hurn" , "Leeming" , "Leuchars" , "Camborne"]

fig, (ax1,ax2,ax3) = plt.subplots(ncols=3,nrows=1 , subplot_kw={"projection" : "3d"})

# This function gets the data and modifies it into monthly data
# Needed a function because sometimes this is done twice in the same time
def get_modified_data(name, time):
    # Read in the excel sheet - the data begins the first 5 rows
        data = pd.read_excel("weather_data.xls", sheet_name=f"{name} May-Oct {time}", skiprows=5)
        
        # Kill the last 4 rows, they're not actually data
        data = data.drop(index=data.tail(4).index)
   
        # I want to remove the units off the names so it's easier to address them
        old_column_names = list( data.columns )
        new_column_names = [ trim_units(name) for name in old_column_names  ]

        # Renaming time
        renaming = dict(zip(old_column_names, new_column_names))

        # Doing the renaming
        data = data.rename(columns=renaming)


        # Convert the date strings to datetimes so we can perform a monthly resampling
        data["Date"] = pd.to_datetime( data["Date"] )

        # Set the index to date for resampling
        data = data.set_index("Date")

        # Perform resampling 
        data = data.resample("M").mean()
        
        return data
    

# Put this in a function because we'll do this twice, one for 1987 and one for 2015
def plotit(time,ax, is_normal):

    # Store the data about each location
    name_data = []

    for name in names:

        data = get_modified_data(name, time)
        
        data1987 = None
        if not is_normal:
            data1987 = get_modified_data(name, 1987)

        # Let's get the monthly mean temperature

        if is_normal:
            monthlytemp = list( data["Daily Mean Temperature"] )
            sunshine = list ( data["Daily Total Sunshine"])
        else:
            monthlytemp = list( data["Daily Mean Temperature"].values - data1987["Daily Mean Temperature"].values)
            sunshine = list ( data["Daily Total Sunshine"].values - data1987["Daily Total Sunshine"].values)

        # Gather all of the data for this location and add to the name data
        info_dict_for_this_data = {"name" : name, "monthlytemp" : monthlytemp, "sunshine" : sunshine}
        name_data.append(info_dict_for_this_data)
        
    # Setting up space on the graph - this is just establishing coordinates
    x =  2*np.repeat(np.arange(5), 6)
    y = 2*np.concatenate( [np.arange(6)] * 5 )
    z = np.zeros(30)

    # d is for delta - the width of the bars
    d = np.ones(30)

    my_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["darkred", "yellow", "lime"], N=256) 



    totalmonthlytemp = []
    totalmonthlysunshine = []
    for nm in name_data:
        totalmonthlytemp.extend( nm["monthlytemp"] )
        totalmonthlysunshine.extend( nm["sunshine"] )
        
    totalmonthlytemp = np.asarray(totalmonthlytemp)
    totalmonthlysunshine = np.asarray(totalmonthlysunshine)


        
    # The plot itself, now that all the data has been initialised and collected
    if is_normal:
        norm = mcolors.Normalize(vmin=totalmonthlysunshine.min(), vmax=totalmonthlysunshine.max())
        the_bars = ax.bar3d(x, y, z, d, d, totalmonthlytemp,color=my_cmap(norm( totalmonthlysunshine) ), cmap = my_cmap, alpha=0.75)
    else:
        norm = mcolors.Normalize(vmin=-3, vmax=3)
        the_bars = ax.bar3d(x, y, z, d, d, totalmonthlytemp,color=redbluecmap(norm( totalmonthlytemp) ), cmap = my_cmap, alpha=0.75)
        ax.set_zlim(totalmonthlytemp.min(), totalmonthlytemp.max())
        
        xs = np.arange(5*2)
        ys = np.arange(6*2)
        X,Y = np.meshgrid(xs,ys)
        def f(x,y):
            return x-x 
        ax.plot_surface(X,Y,f(X,Y), color="orange" , alpha=0.5)

    # For some reason it doesn't work unless I add one before the names
    ax.set_yticklabels(["placeholder", "May","June","July","August","September","October"])
    ax.set_xticklabels(["placeholder"] +  names)

    if ax == ax2:
        required_ticklabels = np.round( np.linspace(totalmonthlysunshine.min(), totalmonthlysunshine.max() , 6),
                                       decimals=2)
        bar = plt.colorbar(mappable=the_bars, 
                           extend="both", 
                           label = "Mean monthly total sunshine (hrs)", 
                           orientation="horizontal",
                           fraction=0.046, pad=0.04)
        bar.set_ticklabels(required_ticklabels)



    ax.set_xlabel("Location")
    ax.set_ylabel("Month")
    if is_normal:
        ax.set_zlabel("Mean temperature (°C)")
        ax.set_title(f"{time}")
    else:
        ax.set_zlabel("Mean temperature change (°C)")
        ax.set_title("Mean difference, 1987-2015")



# Create a custom tick formatter for the z-axis
def z_tick_formatter(x, pos):
    if x >= 0:
        return f'+{x:.1f}'
    else:
        return f'{x:.1f}'

z_formatter = FuncFormatter(z_tick_formatter)
ax3.zaxis.set_major_formatter(z_formatter)

    

plotit(1987,ax1,is_normal = True)
plotit(2015,ax2,is_normal =True)
plotit(2015,ax3, is_normal =False)





plt.suptitle("Comparing mean temperatures across the UK in 1987 with 2015", fontsize=18)







plt.show()


