import pandas as pd
import matplotlib.pyplot as plt
from shared_functions import trim_units, shorten_column_names

# The purpose of this program is to compare various statistics of a location, by comparing the data collected in 1987 with that of 2015
# To do this we'll use boxplots as a more visual way to see the differences, rather than just looking at numbers

# Get the data from a place and time in the large data set, then modify it so it's useable
def get_modified_data(place, time):
    
    data = pd.read_excel("weather_data.xls", sheet_name=f"{place} May-Oct {time}", skiprows=5)
    
    # Kill the last 4 rows, they're not actually data
    data = data.drop(index=data.tail(4).index)

    # Now shorten the column names so they're easy to refer to later on in the program
    data = shorten_column_names(data)
    
    return data

# Where we'll be taking our data from
# Valid locations are the 5 UK weather stations + Jacksonville, Perth, Beijing
placename="Beijing"

# Ratio of pixels to inches
px = 1/96

# Get the data from both time periods
place1987 = get_modified_data(placename, 1987)
place2015 = get_modified_data(placename, 2015)

fig , ((ax1,ax2),(ax3,ax4)) = plt.subplots(ncols=2,
                                           nrows=2, 
                                           figsize=(1920*px,1080*px))

# Collect them in a list so we can refer to them easily
# We're going to be performing a LOT of repetitive operations, so we'll need a loop
axes = [ax1,ax2,ax3,ax4]
  
# Ditto, need to list them so we can iterate over them
quantitystrings = ["Daily Mean Air Temperature","Rainfall" ,"Daily Mean Pressure",  "Daily Mean Wind Speed" ]
units = ["(°C)","(mm) (log)","(hPa)","(kn)"]
# I wanted to get outlier colours that were associated with the quantities, e.g temperature=red, rainfall=blue
outliercolours = ["red","blue","brown","turquoise"]

# It's iteration time
for i in range(4):
    
    # Get the current axis
    ax = axes[i]
    
    # Remove y-axis tick lines (keep tick labels)
    ax.tick_params(axis='y', which='both', left=False)
    
    # Grab the data!
    data1987 = place1987[quantitystrings[i]]
    data2015 = place2015[quantitystrings[i]]
    
    # Perform the plotting with the given specifications
    this_boxplot = ax.boxplot([data1987, data2015], 
                              vert=False, 
                              showmeans=True,
                              medianprops={'color': outliercolours[i]},
                              flierprops = dict(marker='x', markeredgecolor=outliercolours[i])) 
    
    # This is the benefit of adding in a loop - no need to write the same code 4 times, just address via array
    ax.set_title(quantitystrings[i] + " " + units[i])
    ax.set_yticklabels(["1987","2015"])
    
    # Rainfall must be in logscale since that's what the data tends to
    if i==1:
        ax.semilogx()
    
title = plt.suptitle(f"Comparing statistics of {placename} in 1987 with 2015", fontsize=18)
    
# Get the coordinates of the title so we can write some text underneath
title_x,title_y = title.get_position()
    
# (self) explanatory text
fig.text(title_x-0.05, title_y - 0.05, "(green triangle denotes the mean)")

plt.savefig(f"{placename} box plots.png")
    
plt.show()   


