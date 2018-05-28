#!python
from bs4 import BeautifulSoup
import re
import requests
import psycopg2
from tqdm import tqdm
tqdm.monitor_interval = 0
from uuid import UUID


def get_data(file_name):
    with open(file_name) as f:
        for line in tqdm(f):
            import_data(line)        

def import_data(line):
    line = line.split()
    uuid = line[0]
    subject = line[2]
    catalog_nbr  = line[3]
    day = line[4]
    term = line[7]
    section = line[1]
    sql = "INSERT INTO days_offered(course_id, day, subject, catalog_nbr,  section, stream) VALUES(%s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (uuid, day, subject, catalog_nbr, section, term))













if __name__ == '__main__':
    dsn = "postgres://csc394:password@35.188.8.242:5432/csc394"
    conn = psycopg2.connect(dsn)
    global cur 
    cur = conn.cursor()
    file_name = "class_data.txt"
    get_data(file_name)
    conn.commit()
    conn.close()

    
