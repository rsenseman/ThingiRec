from selenium import webdriver
import pandas as pd


def scrape_range(range_tup)
    pinshape_item_data = pd.DataFrame([['itemid','item_name','description','userid','username']])

    driver = webdriver.Firefox()

    for i in xrange(range_tup[0],range_tup[1]):

        if i%500 == 0:
            print i
            print "{} Records collected since last cache".format(len(pinshape_item_data))

            pinshape_item_data.to_csv('item_data_cache_{}.csv'.format(i), encoding = 'utf-8')

            del pinshape_item_data
            pinshape_item_data = pd.DataFrame([['itemid','item_name','description','userid','username']])

        try:
            driver.get("https://pinshape.com/items/{}".format(i))
            name = driver.find_element_by_id('design-name')
            item_name = name.text

            user = driver.find_element_by_class_name('designed-by')
            user_text = user.text
            username = user_text[11:].strip() # Remove initial text "Designed by" and strip whitespace

            id_elem = user.find_element_by_tag_name('a')
            id_string = id_elem.get_attribute('href')
            userid = id_string.split('/')[-1].split('-')[0]

            desc = driver.find_elements_by_xpath('//html/body/div/section/div/div/section/div')
            description = desc[5].text

            pinshape_item_data = pinshape_item_data.append([[i, item_name, description, userid, username]])

        except:
            continue

    pinshape_item_data.to_csv('item_data_cache_{}.csv'.format('final'), encoding = 'utf-8')

    driver.close()

    return None

if __name__ == '__main__':
    scrape_range((14000,15500))
