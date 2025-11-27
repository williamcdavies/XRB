import pandas as pd

#cleanup:
#adding alpha, nu, E_1measured, E_2measured, gamma, and time columns with default values 
#to allow for conversion between X-ray energy bands and radio frequencies and to allow
#for time evolution plots
#additionally, 0.0s are replaced before the time column is added to differentiate between deliberate 0.0
#and unknown values. inf will be our typical placeholder here
def cleanup(filename):
    #read in the original file exactly
    df = pd.read_csv(
        filename,
        dtype=str,           
        na_filter=False    
    )
    
    df = df.replace('0.0', float('inf'))
    df = df.replace('None', 'NULL')
    df['alpha'] = 0
    df['nu'] = 5
    df['E_1measured'] = 1
    df['E_2measured'] = 10
    df['gamma'] = 1.7
    df['time'] = 0.0

    new_col_order = ['Name','Class','Lr','Lr_ler','Lr_uer','Lx','Lx_ler','Lx_uer',
                    'uplim','alpha','nu','E_1measured','E_2measured','gamma','time','Ref']
    df = df[new_col_order]
    df.to_csv('clean_data/lrlx_data_BH_CLEAN.csv', index=False)
    return df

df = cleanup('original_data/lrlx_data_BHs.csv')