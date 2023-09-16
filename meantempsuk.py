import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter

redbluecmap = plt.get_cmap("seismic")

# Size of one pixel in inches
px = 1/96

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

# Names of the 5 weather stations in a cherrypicked order so that our plots look more smooth
stations = ["Leuchars" , "Leeming" , "Camborne" , "Hurn" , "Heathrow"]

fig, (ax1,ax2,ax3) = plt.subplots(ncols=3,
                                  nrows=1 , 
                                  figsize=(1920*px, 1080*px), 
                                  subplot_kw={"projection" : "3d"})

# This function gets the data and modifies it into monthly data, also makes some qol changes to the data
# Needed a function because sometimes this needs to be done in different contexts
def get_modified_data(name, time):
        # Read in the excel sheet - the data begins the first 5 rows
        data = pd.read_excel("weather_data.xls", sheet_name=f"{name} May-Oct {time}", skiprows=5, na_values = ["n/a"])
        
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

        # Perform resampling - monthly and get the monthly mean data from the columns we care about
        data = data.resample("M").agg({ "Daily Mean Temperature" : "mean" , 
                                       "Daily Total Sunshine" : "mean"})
        
        return data
    

# Put this in a function because we'll do this twice, one for 1987 and one for 2015
# Edit: and a third time for the temp difference. The is_normal parameter is for if we're plotting the temperatures as usual
# or instead plotting the temp differences (the third graph is for the differences)
# the ax argument is just which axis you want to plot it on
def plotit(time,ax, is_normal):

    # Store the data about each location
    name_data = []

    for station in stations:

        data = get_modified_data(station, time)
        
        data1987 = None
        if not is_normal:
            data1987 = get_modified_data(station, 1987)

        # Let's get the monthly mean temperature

        if is_normal:
            monthlytemp = list( data["Daily Mean Temperature"] )
            sunshine = list ( data["Daily Total Sunshine"])
        else:
            monthlytemp = list( data["Daily Mean Temperature"].values - data1987["Daily Mean Temperature"].values)
            sunshine = list ( data["Daily Total Sunshine"].values - data1987["Daily Total Sunshine"].values)

        # Gather all of the data for this location and add to the name data
        info_dict_for_this_data = {"name" : station, "monthlytemp" : monthlytemp, "sunshine" : sunshine}
        name_data.append(info_dict_for_this_data)
        
    # Setting up space on the graph - this is just establishing coordinates
    x =  2*np.repeat(np.arange(5), 6)
    y = 2*np.concatenate( [np.arange(6)] * 5 )
    z = np.zeros(30)

    # d is for delta - the width and thickness of the bars (should be the same)
    d = np.ones(30)

    # This is for daily total sunshine
    my_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["darkred", "yellow", "lime"], N=256) 


    # These lists will store the full list of temperatures and sunshines from all 5 locations
    # Didn't want to use numpy here since I felt more confident using native python for this specific task
    totalmonthlytemp = []
    totalmonthlysunshine = []
    for nm in name_data:
        totalmonthlytemp += nm["monthlytemp"] 
        totalmonthlysunshine += nm["sunshine"] 
        
    # Once we have the lists, turn into numpy arrays for speed + numpy methods
    totalmonthlytemp = np.asarray(totalmonthlytemp)
    totalmonthlysunshine = np.asarray(totalmonthlysunshine)


        
    # The plot itself, now that all the data has been initialised and collected
    if is_normal:
        norm = mcolors.Normalize(vmin=totalmonthlysunshine.min(), vmax=totalmonthlysunshine.max())
        the_bars = ax.bar3d(x, y, z, d, d, totalmonthlytemp,color=my_cmap(norm( totalmonthlysunshine) ), cmap = my_cmap, alpha = 0.75   )
    else:
        # This norm is for the temperatures - I want 0 to be fully neutral so need to make the extrema symmetrical
        norm = mcolors.Normalize(vmin=-3, vmax=3)
        the_bars = ax.bar3d(x, y, z, d, d, totalmonthlytemp,color=redbluecmap(norm( totalmonthlytemp) ), cmap = my_cmap, alpha=0.75)
        
        # Need to set this limit so that when we get negative values they don't go underneath the chart
        ax.set_zlim(totalmonthlytemp.min(), totalmonthlytemp.max())
        
        # This code will be used to generate a plane that cuts across x,y=0 so that we can see more easily where temperatures have risen
        # and where they have fallen
        xs = np.arange(5*2)
        ys = np.arange(6*2)
        X,Y = np.meshgrid(xs,ys)
        
        # I wanted 0 but if you just put 0 then it won't work since it's a number, so if we do x-x we can get 0 in the required form 
        f = lambda x,y : x-x
        
        # Plot the plane. I chose gold as an intermediary between red (hot) and blue (cold)
        zero_bound = ax.plot_surface(X,Y,f(X,Y), color="gold" , alpha=0.5)

    # For some reason it doesn't work unless I add one before the names
    ax.set_yticklabels(["placeholder", "May","June","July","Aug.","Sept.","Oct."])
    ax.set_xticklabels(["placeholder"] +  stations)

    # ax2 is in the middle so I thought that's the best place to put the colourbar
    if ax == ax2:
        # Since the data was colour-normalised I need to set the sunshine ticks manually or it'll just go from 0-1 
        # Round to stop stupid floating point errors
        required_ticklabels = np.round( np.linspace(totalmonthlysunshine.min(), totalmonthlysunshine.max() , 6),
                                       decimals=2)
        bar = plt.colorbar(mappable=the_bars, 
                           extend="both", 
                           label = "Mean daily total sunshine (hrs)", 
                           orientation="horizontal",
                           fraction=0.046, pad=0.04) # Magic numbers, make the colourbar fit proportionally - got them from stackoverflow
        bar.set_ticklabels(required_ticklabels)


    ax.set_xlabel("Location")
    ax.set_ylabel("Month")
    
    # Need to make sure our axes have been labelled accordingly - the temperature change plot should have different labels
    # I could've done this manually after plotting but would've taken longer and I wanted direct access to the axes
    if is_normal:
        ax.set_zlabel("Mean temperature (°C)")
        ax.set_title(f"{time}")
    else:
        ax.set_zlabel("Mean temperature change (°C)")
        ax.set_title("Temperature difference, 1987-2015")


# This code was copied from chatGPT, I wanted to put a + on all the positive values to show it's a positive change in temperature
# But doing this required importing a module and lots of work so just let chatGPT do it for me
# Create a custom tick formatter for the z-axis
def z_tick_formatter(x, pos):
    if x >= 0:
        return f'+{x:.1f}'
    else:
        return f'{x:.1f}'

z_formatter = FuncFormatter(z_tick_formatter)
ax3.zaxis.set_major_formatter(z_formatter)

# The third one is the temperature change graph
plotit(1987,ax1,is_normal = True)
plotit(2015,ax2,is_normal =True)
plotit(2015,ax3, is_normal =False)

plt.suptitle("Comparing mean temperatures across the UK in 1987 with 2015", fontsize=18)

plt.savefig("weatherdiagram.png")

plt.show()


