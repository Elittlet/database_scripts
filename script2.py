#!python
from bs4 import BeautifulSoup
import re
import requests
import psycopg2
from tqdm import tqdm
tqdm.monitor_interval = 0


def get_info(course_nbr, subject, term, id): 
    url = 'https://offices.depaul.edu/_layouts/DUC.SR.ClassSvc/DUClassSvc.ashx?action=getclasses&strm='+str(term)+'&subject='+str(subject)+'&catalog_nbr='+str(course_nbr)
    payload = requests.get(url).json()
    if not payload:
        return
    else:
        import_info(course_nbr, subject, payload, id, term)


def get_day(payload):
    days = ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat']
    for day in days:
        if payload[day] == "Y":
            return day
    


def get_time(payload_time):
    #print(payload_time.split())
    if payload_time != "":
        time = payload_time.split()[1] + payload_time.split()[2]
    else:
        time = "N/A"
    return time

def import_info(course_nbr, subject, payload, id, term):
    for i in payload:
        if i["location_descr"] == "Study Abroad":
            return
        elif i["location_descr"] == "OnLine":
            start_time = "OnLine"
            end_time = "OnLine"
            day = "OnLine"
        else:
            start_time = get_time(i['meeting_time_start'])
            end_time = get_time(i['meeting_time_end'])
            day = get_day(i)
        section_nbr = i['class_section']
        class_nbr = i['class_nbr']
        
        if not start_time and not end_time:
            start_time = "N/A"
            end_time = "N/A"
        if not day:
            day = "N/A"

        with open('class_data.txt', 'a+') as f:
            line = str(id+ ' '+ section_nbr +' '+ subject +' '+ str(course_nbr) +' '+ day +' '+ start_time +' '+ end_time + ' ' + term + '\n')
            if line in f:
                pass
            else:
                f.write(line)
            f.close()



if __name__ == "__main__":
    pbar = tqdm(total=286, initial=0)
    dsn = "postgres://csc394:password@35.188.8.242:5432/csc394"
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute("SELECT title, subject, course_nbr, id  FROM csc394_courses  ORDER BY course_nbr")
    row = cur.fetchone()
    terms = ['1005', '1000', '0995', '0990', '0985', '0980', '0975']
    
    while row is not None:
        subject = row[1]
        course_nbr = row[2]
        id = row[3]
        for term in terms:
            payload = get_info(course_nbr, subject, term, id)
        pbar.update(1)
        row = cur.fetchone()
    cur.close()


    
