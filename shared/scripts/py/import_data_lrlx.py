import psycopg
import csv
import os

def check_none(val):
    return val if (val != "inf" and val != "NULL" and "<" not in val and ">" not in val) else None

with open("shared/data/clean_data/lrlx_data_BH_CLEAN.csv", mode="r", newline="") as lrlx_csv:
    csv_reader = csv.reader(lrlx_csv)
    
    next(csv_reader)
    
    data_to_insert = []
    for row in csv_reader:
        
        name = check_none(row[0])
        classification = check_none(row[1])
        lr = check_none(row[2])
        lr_ler = check_none(row[3])
        lr_uer = check_none(row[4])
        lx = check_none(row[5])
        lx_ler = check_none(row[6])
        lx_uer = check_none(row[7])
        uplink = check_none(row[8])
        alpha = check_none(row[9])
        nu = check_none(row[10])
        e1_measured = check_none(row[11])
        e2_measured = check_none(row[12])
        gamma = check_none(row[13])
        time = check_none(row[14])
        ref = check_none(row[15])
        
        insert_row = (name, classification, lr, lr_ler, lr_uer, lx, lx_ler, lx_uer, uplink, alpha, nu, e1_measured, e2_measured, gamma, time, ref)
        data_to_insert.append(insert_row)
    
    with psycopg.connect(f"host=localhost dbname=xrb user={os.getenv('POSTGRES_USER')} password={os.getenv('POSTGRES_PASSWORD')}") as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO lrlx_data (name, class, lr, lr_ler, lr_uer, lx, lx_ler, lx_uer, uplim, alpha, nu, e1_measured, e2_measured, gamma, time, ref)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, data_to_insert)