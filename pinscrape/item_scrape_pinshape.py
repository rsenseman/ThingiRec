from selenium import webdriver
import pandas as pd

def get_most_recent_item_id():
    driver = webdriver.Firefox()

    driver.get("https://pinshape.com/3d-marketplace?sort-by=newest")
    new_items = driver.find_elements_by_xpath("//html/body/div/section/div/div/ul/li")
    newest_item_id = new_items[0].get_attribute("id")

    driver.close()

    return int(newest_item_id)

def scrape_pinshape_page(driver, i):
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

        return i, item_name, description, userid, username

    except:
        return None

def scrape_range(min_item_id, max_item_id):
    pinshape_item_data = pd.DataFrame([['itemid','item_name','description','userid','username']])

    driver = webdriver.Firefox()

    for i in xrange(min_item_id, max_item_id + 1):

        if i%500 == 0:
            # Every 500 items, backup records to csv
            print "{} Records collected".format(len(pinshape_item_data))

            pinshape_item_data.to_csv('item_data_backup_{}.csv'.format(i), encoding = 'utf-8')

            pinshape_item_data = pd.DataFrame([['itemid','item_name','description','userid','username']])

        new_item_data = scrape_pinshape_page(driver, i)

        if new_item_data:
            i, item_name, description, userid, username = new_item_data
            pinshape_item_data = pinshape_item_data.append([[i, item_name, description, userid, username]])
        else:
            continue

    pinshape_item_data.to_csv('item_data_backup_{}.csv'.format('final'), encoding = 'utf-8')

    driver.close()

    return None

if __name__ == '__main__':
    max_item_id = get_most_recent_item_id()
    scrape_range(0,max_item_id)
