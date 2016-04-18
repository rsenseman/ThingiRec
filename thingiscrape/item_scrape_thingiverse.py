import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def scrape_range(range_tup, sleep_time)
    thingiverse_item_data = pd.DataFrame([['itemid','item_name','description','username']])

    for i in xrange(range_tup[0],range_tup[1]):
        if i%500 == 0:
            print i
            print "{} Records collected since last cache".format(len(pinshape_item_data))

            thingiverse_item_data.to_csv('thingi_item_data_cache_{}.csv'.format(i), encoding = 'utf-8')

            del thingiverse_item_data
            thingiverse_item_data = pd.DataFrame([['itemid','item_name','description','username']])

        try:
            res = requests.get('http://www.thingiverse.com/thing:{}'.format(i))
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')

            thing_name = soup.select('div[class="thing-header-data"]')
            item_name = thing_name[0].text.split('by')[0].strip()
            username[0].text.split('by')[1][1:-102]

            thing_page = soup.select('div[id="thing-page"]')
            item_id = thing_page[0].attrs['data-thing-id']

            description_object = soup.select('div[id="description"]')
            item_description = "".join(description_object[0].text.split('\n'))[7:]

            thingiverse_item_data = thingiverse_item_data.append([[item_id, item_name, item_description, username]])

            time.sleep(float(sleep_time))
        except:
            continue

    thingiverse_item_data.to_csv('thingi_item_data_cache_{}.csv'.format('final'), encoding = 'utf-8')

    thingiverse_item_data.tail()

if __name__ == '__main__':
    scrape_range((14000,15500))
