from time import sleep
from selenium import webdriver
from lxml.html import fromstring

data = {}

path_to_chrome = '/home/brutal/Desktop/chromedriver'

driver = webdriver.Chrome(executable_path = path_to_chrome)  # i.e '/home/superman/www/myproject/chromedriver'
driver.get('https://www.gianteagle.com/Pharmacy/Savings/4-10-Dollar-Drug-Program/Generic-Drug-Program/')

# Loop states
for i in range(2, 7):
    dropdown_state = driver.find_element(by='id', value='ctl00_RegionPage_RegionPageMainContent_RegionPageContent_userControl_StateList')

    # open dropdown
    dropdown_state.click()

    # click state
    driver.find_element_by_xpath('//*[@id="ctl00_RegionPage_RegionPageMainContent_RegionPageContent_userControl_StateList"]/option['+str(i)+']').click()

    # let download the page
    sleep(3)

    # prepare HTML
    page_content = driver.page_source #helps to get the souce code of the current page
    tree = fromstring(page_content)

    state = tree.xpath('//*[@id="ctl00_RegionPage_RegionPageMainContent_RegionPageContent_userControl_StateList"]/option['+str(i)+']/text()')[0]
    data[state] = []

    # Loop products inside the state
    for line in tree.xpath('//*[@id="ctl00_RegionPage_RegionPageMainContent_RegionPageContent_userControl_gridSearchResults"]/tbody/tr[@style]'):
        med_type = line.xpath('normalize-space(.//td[@class="medication-type"])')
        generic_name = line.xpath('normalize-space(.//td[@class="generic-name"])')

        brand_name = line.xpath('normalize-space(.//td[@class="brand-name hidden-xs"])')
        strength = line.xpath('normalize-space(.//td[@class="strength"])')
        form = line.xpath('normalize-space(.//td[@class="form"])')

        qty_30_day = line.xpath('normalize-space(.//td[@class="30-qty"])')
        price_30_day = line.xpath('normalize-space(.//td[@class="30-price"])')

        qty_90_day = line.xpath('normalize-space(.//td[@class="90-qty hidden-xs"])')
        price_90_day = line.xpath('normalize-space(.//td[@class="90-price hidden-xs"])')

        data[state].append(dict(med_type=med_type,
                                generic_name=generic_name,
                                brand_name=brand_name,
                                strength=strength,
                                form=form,
                                qty_30_day=qty_30_day,
                                price_30_day=price_30_day,
                                qty_90_day=qty_90_day,
                                price_90_day=price_90_day))

states = ['Indiana','Ohio','Maryland','West Virginia','Pennsylvania']
for state in states:
    print(state)
    for i in data[state]:
        print(i)
        print('\n')
    
driver.quit()

