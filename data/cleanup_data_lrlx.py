import pandas as pd

#data cleanup:
#adding alpha, nu, E_1meausred, E_2measured, gamma, and time columns with default vaules 
#to allow for conversion between X-ray energy bands and radio frequencies and to allow
#for time evolution plots
def cleanup(filename):
    df = pd.read_csv(filename, dtype=str)  # everything will be strings, conversion will be done during visualization

    pd.options.display.float_format = "{:.3e}".format
    df['alpha'] = 0
    df['nu'] = 5e9
    df['E_1measured'] = 1e3
    df['E_2measured'] = 1e4
    df['gamma'] = 1.7
    df['time'] = 0.0

    df.to_csv('lrlx_data_BH_CLEAN.csv', index=False)
    return df

df = cleanup('lrlx_data_BHs.csv')

