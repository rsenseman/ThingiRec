import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import psycopg2

def insert_into_database(data, connection, cursor):

    SQL = "INSERT INTO thingi_items (item_id, item_name, description, username) \
       VALUES (%s, %s, %s, %s);"

    cursor.execute(SQL, data)
    connection.commit()

    return None

def scrape_thingiverse_page(i):
    try:
        res = requests.get('http://www.thingiverse.com/thing:{}'.format(i))
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')

        thing_name = soup.select('div[class="thing-header-data"]')
        item_name = thing_name[0].text.split('by')[0].strip()
        username = thing_name[0].text.split('by')[1].split(',')[0][1:]

        item_id = i

        description_object = soup.select('div[id="description"]')
        item_description = "".join(description_object[0].text.split('\n'))[7:]
        item_description = item_description.replace('.Instructions', ' ')

        print "{} collected: {}".format(i, item_name)
        return item_id, item_name, item_description, username

    except:
        print "{} ...".format(i)
        return None

def scrape_range(range_tup, sleep_time, db_connection, db_cursor):

    thingiverse_item_data = pd.DataFrame([['itemid','item_name','description','username']])

    for i in xrange(range_tup[0],range_tup[1]):

        time.sleep(float(sleep_time))

        if i%100000 == 0:
            # Every 100000 items, backup records to local csv
            print i
            print "{} records collected".format(len(thingiverse_item_data))

            thingiverse_item_data.to_csv('thingi_item_data_backup_{}.csv'.format(i), encoding = 'utf-8')

            thingiverse_item_data = pd.DataFrame([['itemid','item_name','description','username']])

        new_item_data = scrape_thingiverse_page(i)

        if new_item_data:
            item_id, item_name, item_description, username = new_item_data
            thingiverse_item_data = thingiverse_item_data.append([[item_id, item_name, item_description, username]])
            insert_into_database((item_id, item_name, item_description, username), db_connection, db_cursor)
        else:
            continue

    thingiverse_item_data.to_csv('thingi_item_data_backup_{}.csv'.format('final'), encoding = 'utf-8')

    return None

if __name__ == '__main__':
    conn = psycopg2.connect(dbname='thingiscrape', user='robert', host='/tmp')
    c = conn.cursor()

    scrape_range((4433,1506586), 2, conn, c)

    conn.close()
