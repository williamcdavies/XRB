import psycopg
import csv
import os

def check_null_or_inf(val):
    return val if (val != "inf" and val != "NULL" and "<" not in val and ">" not in val) else None

with open("shared/data/clean_data/xrb_properties_CLEAN.csv", mode="r", newline="") as xrb_csv:
    csv_reader = csv.reader(xrb_csv)
    
    next(csv_reader)
    
    data_to_insert = []
    for row in csv_reader:
        
        name                = row[0]
        distance            = check_null_or_inf(row[1])
        distance_err        = check_null_or_inf(row[2])
        rl                  = check_null_or_inf(row[3])
        incl                = check_null_or_inf(row[4])
        incl_err            = check_null_or_inf(row[5])
        hard_line_slope     = check_null_or_inf(row[6])
        hard_line_slope_err = check_null_or_inf(row[7])
        spec_type           = check_null_or_inf(row[8])
        p_orb               = check_null_or_inf(row[9])
        mass                = check_null_or_inf(row[10])
        
        insert_row = (name, distance, distance_err, rl, incl, incl_err, hard_line_slope, hard_line_slope_err, spec_type, p_orb, mass)
        data_to_insert.append(insert_row)
    
    with psycopg.connect(f"host=localhost dbname=xrb user={os.getenv('POSTGRES_USER')} password={os.getenv('POSTGRES_PASSWORD')}") as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO xrb_properties (name, distance, distance_err, rl, incl, incl_err, hard_line_slope, hard_line_slope_err, spec_type, p_orb, mass)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data_to_insert)