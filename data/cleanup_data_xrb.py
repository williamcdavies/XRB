import pandas as pd

#data cleanup:
#adding alpha, nu, E_1meausred, E_2measured, gamma, and time columns with default vaules 
#to allow for conversion between X-ray energy bands and radio frequencies and to allow
#for time evolution plots
def cleanup(filename):
    df = pd.read_csv(filename, dtype=str)  # everything will be strings, conversion will be done during visualization

   

    df.to_csv('xrb_properties_CLEAN.csv', index=False)
    return df

df = cleanup('xrb_properties.csv')

