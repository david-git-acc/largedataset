import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from shared_functions import shorten_column_names

# The purpose of this program is to compare different statistics about a place in the UK in a certain time to check for correlations
# We'll be using a regression plane to try and identify a linear relationship

# Weather station to check
# Suitable stations are Hurn, Heathrow, Camborne, Leeming, Leuchars
name="Camborne"
time=1987

# Pixel-to-inch ratio
px =1/96

fig, ax= plt.subplots(ncols=1,
                      nrows=1, 
                      figsize=(1440*px, 1080*px),
                      subplot_kw={"projection":"3d"})

# Function to plot this. I made it a function so it's easy to plot multiple graphs
def plotit(ax, place):
    
    # Make the plot global so our colourbar can access it later
    global scattering

    # Getting the data and cleaning null values
    stationdata = pd.read_excel("weather_data.xls" , 
                                sheet_name=f"{place} May-Oct {time}" , 
                                skiprows=5, 
                                na_values=["n/a","tr"])
    stationdata = stationdata.fillna(0)

    # The last 4 columns aren't data, just background info 
    stationdata = stationdata.drop(index= stationdata.tail(4).index)

    # Shorten the column names so it's less boring to refer to them
    stationdata = shorten_column_names(stationdata)

    visibility = stationdata["Daily Mean Visibility"].values
    pressures = stationdata["Daily Mean Pressure"].values
    windspeeds = stationdata["Daily Mean Windspeed"].values[:, 0]
    cloudcover = stationdata["Daily Mean Total Cloud"].values   

    # This is for daily cloud cover
    cloud_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["navy","cyan"], N=256).reversed()
    norm = mcolors.Normalize(vmin = cloudcover.min(), vmax = cloudcover.max())

    # Plotting the data
    scattering = ax.scatter( visibility, pressures, windspeeds, 
                            c=norm(cloudcover),
                            cmap=cloud_cmap,
                            s=32,
                            edgecolor="black")
    
    # REGRESSION PLANE CALCULATION
    # I will let numpy do the work.
    # x-axis = visibility, y-axis = pressure, z-axis = windspeed
    # want to construct a regression plane of the form z = ax + by + c, find coefficients a,b,c to minimise error
    
    # This is our matrix that we need to solve for using the least squares method
    A = np.column_stack((visibility, pressures, np.ones_like(visibility)))
    
    # Get numpy to do all the work, returning the coefficients
    # The coefficients will be an ndarray contained in the first element of the overall returned array - use unpacking
    # Had to use asfloat to prevent "same kind" casting error
    a,b,c = np.linalg.lstsq(A.astype('float'), windspeeds.astype('float'), rcond=False)[0]
    
    print((a,b,c))
    
    # Our linear regression plane
    regplane = lambda x,y: a*x + b*y + c
    
    # Resolution for our plane (number of points we will plot per axis) - it's a flat surface so we can get away with a low number
    res = 10
    
    # These get the bounds of our x and y dimensions, so we can use it to plot our 3D plane using meshgrid
    xextents = np.linspace(visibility.min(), visibility.max(), res)
    yextents = np.linspace(pressures.min(), pressures.max() , res)
    
    # The x-y grid we'll plot our function on
    X,Y = np.meshgrid(xextents,yextents)
    
    # Plotting the plane itself
    the_plane = ax.plot_surface(X,Y,regplane(X,Y) , color="blue", alpha=0.25)

    ax.set_xlabel("D.M. Visibility (dm)")
    ax.set_ylabel("D.M. Pressure (hPa)")
    ax.set_zlabel("D.M. Windspeed (kn)")
    
    # Used for formatting when showing the title
    plusorminus = lambda x : "+" if x > 0 else "-"
    
    # All this formatting to avoid seeing "+-" in the title
    ax.set_title(f"regression: z = {a:.3f}x {plusorminus(b)} {abs(b):.2f}y {plusorminus(c)} {abs(c):.2f}")


plotit(ax, name)


# The scatter plot's colours are normalised, so the bar's ticks will go from 0 to 1
# This is obviously not correct, so we will need to set the ticks manually
requiredbarticks = np.round( np.linspace(0,8, 6), decimals=2)

# Defining the colourbar
bar = plt.colorbar(
                   mappable=scattering, 
                   extend="both", 
                   orientation="horizontal",
                   label="Daily Mean Total Cloud (oktas)", 
                   fraction=0.046, # Magic numbers from stackoverflow, they balance the size of the bar
                   pad=0.04,
                   )

# Setting the tick labels
bar.set_ticklabels(requiredbarticks)

plt.suptitle(f"Comparing daily mean visibility, daily mean pressure and daily mean windspeed in {name}, {time}", fontsize=18)

plt.savefig("windy.png")

plt.show()