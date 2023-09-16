# This is the place to store functions used across multiple programs to avoid data redundancy

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

# Rename columns so that I don't have to write the exact full names from the large data set
def shorten_column_names(data):
    
    # I want to remove the units off the names so it's easier to address them
    old_column_names = list( data.columns )
    new_column_names = [ trim_units(name) for name in old_column_names  ]

    # Renaming time
    renaming = dict(zip(old_column_names, new_column_names))

    # Doing the renaming
    data = data.rename(columns=renaming)

    return data
    