import pandas as pd

#data cleanup:
#replacing '-9000' entries with the float representation of infinity,
#'unknown' entries with NULL
def cleanup(filename):
    df = pd.read_csv(filename, dtype=str)  # everything will be strings, conversion will be done during visualization

    df = df.replace('-9000', float('inf'))
    df = df.replace('unknown', 'NULL')

    df.to_csv('clean_data/xrb_properties_CLEAN.csv', index=False)
    return df

df = cleanup('original_data/xrb_properties.csv')

