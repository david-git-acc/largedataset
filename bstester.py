import pandas as pd
import numpy as np

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

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

        # Perform resampling - monthly
        data = data.resample("M").mean(numeric_only=False)
        
        return data
    
    
leeming = get_modified_data("Leeming" , 1987)
leuchars=get_modified_data("Leuchars" , 1987)
hurn=get_modified_data("Hurn" , 1987)
heathrow=get_modified_data("Heathrow" , 1987)
camborne = get_modified_data("Camborne" , 1987)

print(leeming["Daily Mean Temperature"]["1987-06-30"])
print(leuchars["Daily Mean Temperature"]["1987-06-30"])
print(hurn["Daily Mean Temperature"]["1987-06-30"])
print(heathrow["Daily Mean Temperature"]["1987-06-30"])
print(camborne["Daily Mean Temperature"]["1987-06-30"])