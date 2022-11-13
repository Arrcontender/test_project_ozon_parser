from selenium.webdriver.common.by import By
import pandas as pd
import undetected_chromedriver
from selenium.webdriver.common.action_chains import ActionChains

import time


def init_driver():
    options = undetected_chromedriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument('--headless')
    driver = undetected_chromedriver.Chrome(options=options)
    return driver


class LoadingPages:
    def __init__(self):
        self.links = []
        self.url = 'https://www.ozon.ru/category/smartfony-15502/?sorting=rating'
        self.count = 0


links_obj = LoadingPages()


def get_first_100_urls():
    driver = init_driver()
    driver.get(url=links_obj.url)
    time.sleep(10)
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
                                                             '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[1]/aside/div[6]/div[1]')).perform()
    time.sleep(2)
    blocks = driver.find_elements(By.CLASS_NAME, 'kr5')
    for block in blocks:
        x = block.find_element(By.TAG_NAME, 'a')
        href = x.get_attribute('href')
        links_obj.links.append(href)
    stage = driver.find_element(By.CLASS_NAME, 't9e')
    next_page_block = stage.find_element(By.CLASS_NAME, '_4-a1')
    links_obj.url = next_page_block.get_attribute('href')

    driver.close()
    driver.quit()
    if len(links_obj.links) < 100:
        get_first_100_urls()
    with open('/parsing/pages/original_links.txt', 'w') as file:
        for i in links_obj.links:
            file.write(i + '\n')
    return links_obj.links


def get_op():

    op_list = []

    errors = []

    file = open('/Users/ambrosko/Prog/TestProjectforPyShop/parsing/pages/selected_links.txt') # отобрал 14 ссылок для более быстрого парсинга

    for i in file:
        driver = init_driver()

        driver.get(url=i)
        time.sleep(1.5)
        try:
            ActionChains(driver).\
                click(on_element=driver.find_element(By.XPATH,
                                                     '//*[@id="layoutPage"]/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[3]/div/a')).perform()
            time.sleep(1)
            if 'Apple' in driver.find_element(By.XPATH,
                                              '//*[@id="layoutPage"]/div[1]/div[3]/div[2]/div/div/div[1]/div/h1').text:
                blocks = driver.find_elements(By.CLASS_NAME, 'lx0')
                for block in blocks:
                    if 'Основные' in [x.text for x in block.find_elements(By.TAG_NAME, 'div')]:
                        strings = block.find_elements(By.TAG_NAME, 'a')
                        op_list.append(strings[1].text)

            else:
                blocks = driver.find_elements(By.CLASS_NAME, 'lx0')
                for block in blocks:
                    if 'Общие' in [x.text for x in block.find_elements(By.TAG_NAME, 'div')]:
                        strings = block.find_elements(By.TAG_NAME, 'dd')
                        for string in strings:
                            if 'Android ' in string.text:
                                op_list.append(string.text)

        except:
            print(f'error while parsing {i}\n')
            errors.append(i)

        driver.close()
        driver.quit()
    file.close()
    pd_list = pd.Series(op_list)
    pd_list.value_counts().to_csv('/Users/ambrosko/Prog/TestProjectforPyShop/parsing/statistics/op_statistics.csv',
                                  sep='-', header=False)


if __name__ == '__main__':
    get_first_100_urls()
    get_op()
