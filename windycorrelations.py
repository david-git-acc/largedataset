import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import datetime as dt

name="Leeming"

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

fig, ax= plt.subplots(ncols=1,nrows=1, subplot_kw={"projection":"3d"})

def plotit(ax, place):
    
    global scattering

    stationdata = pd.read_excel("weather_data.xls" , 
                                sheet_name=f"{place} May-Oct 2015" , 
                                skiprows=5, 
                                na_values=["n/a","tr"])
    stationdata = stationdata.fillna(0)

    # The last 4 columns aren't data, just background info 
    stationdata = stationdata.drop(index= stationdata.tail(4).index)

    # I want to remove the units off the names so it's easier to address them
    old_column_names = list( stationdata.columns )
    new_column_names = [ trim_units(name) for name in old_column_names  ]


    # Renaming time
    renaming = dict(zip(old_column_names, new_column_names))
    stationdata = stationdata.rename(columns=renaming)

    visibility = stationdata["Daily Mean Visibility"].values
    pressures = stationdata["Daily Mean Pressure"].values
    windspeeds = stationdata["Daily Mean Windspeed"].values[:, 0]
    cloudcover = stationdata["Daily Mean Total Cloud"].values   

    # This is for daily cloud cover
    cloud_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["navy","cyan"], N=256) 
    norm = mcolors.Normalize(vmin = cloudcover.min(), vmax = cloudcover.max())

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
    
    
    the_plane = ax.plot_surface(X,Y,regplane(X,Y) , color="gold", alpha=0.25)

    ax.set_xlabel("D.M. Visibility (dam)")
    ax.set_ylabel("D.M. Pressure (hPa)")
    ax.set_zlabel("D.M. Windspeed (kn)")
    
    # Used for formatting when showing the title
    plusorminus = lambda x : "+" if x > 0 else "-"
    
    # All this formatting to avoid seeing "+-" in the title
    ax.set_title(f"regression: z = {a:.2f}x {plusorminus(b)} {abs(b):.2f}y {plusorminus(c)} {abs(c):.2f}")


plotit(ax, "Leeming")



requiredbarticks = np.round( np.linspace(0,8, 6), decimals=2)
bar = plt.colorbar(
                   mappable=scattering, 
                   extend="both", 
                   orientation="horizontal",
                   label="Daily Mean Total Cloud (oktas)", 
                   fraction=0.046, 
                   pad=0.04,
                   )




# bar.set_ticklabels(requiredbarticks)

plt.suptitle(f"Comparing daily mean visibility, daily mean pressure and daily mean windspeed in {name}, 2015", fontsize=16)


plt.show()