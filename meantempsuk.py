import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

names = ["Heathrow" , "Hurn" , "Leeming" , "Leuchars" , "Camborne"]

fig, (ax1,ax2) = plt.subplots(ncols=2,nrows=1, subplot_kw={"projection" : "3d"})

# Put this in a function because we'll do this twice, one for 1987 and one for 2015
def plotit(time,ax):

    # Store the data about each location
    name_data = []

    for name in names:


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

        # Let's get the monthly mean temperature

        monthlytemp = list( data["Daily Mean Temperature"] )
        sunshine = list ( data["Daily Total Sunshine"])
        
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

    # Normalize your data to the colormap's range (0 to 1)
    norm = mcolors.Normalize(vmin=totalmonthlysunshine.min(), vmax=totalmonthlysunshine.max())
        
    # The plot itself, now that all the data has been initialised and collected
    the_bars = ax.bar3d(x, y, z, d, d, totalmonthlytemp,color=my_cmap(norm( totalmonthlysunshine) ), cmap = my_cmap)

    # For some reason it doesn't work unless I add one before the names
    ax.set_yticklabels(["placeholder", "May","June","July","August","September","October"])
    ax.set_xticklabels(["placeholder"] +  names)

    # Trying to eliminate the margin between the bottom of the graph and the bars 
    ax.set_zlim(0, totalmonthlytemp.max())

    ax.set_xlabel("Location")
    ax.set_ylabel("Month")
    ax.set_zlabel("Mean temperature (°C)")
    
    ax.set_title(f"{time}")
    

plotit(1987,ax1)
plotit(2015,ax2)

plt.tight_layout()
plt.suptitle("Comparing mean temperatures across the UK in 1987 with 2015", fontsize=20)

# ax3 = fig.add_subplot(113, projection="3d")



plt.show()


