import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class HomeListingSpiderSelenium(scrapy.Spider):
    name = "Homes_Selenium_Spider"
    #start_urls = ['https://www.homes.com/redlands-ca/homes-for-sale/']
    #start_urls = ['https://www.homes.com/grand-junction-co/homes-for-sale/']
    start_urls = ['https://www.homes.com/san-bernardino-ca/homes-for-sale/']
    #start_urls = ['https://www.homes.com/schaumburg-il/homes-for-sale/']
    #start_urls = ['https://www.homes.com/phoenix-az/homes-for-sale/']

    def __init__(self):
        self.driver = webdriver.Chrome('/Users/BrandonKubick/Documents/chromedriver')
        self.driver2 = webdriver.Chrome('/Users/BrandonKubick/Documents/chromedriver')
        self.i = 1
        self.page = 1

    def parse(self, response):
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("-------------------------New Page-----------------------------")
        print('On Page: ' + str(self.page))
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        self.driver.get(response.url)
        time.sleep(5)

        houses = self.driver.find_elements_by_css_selector('div.card-wrapper.card-wrapper--property.grid-cell a')

        for house in houses:
            house_url = house.get_attribute("href")
            yield response.follow(house_url, callback=self.parse_house)


        #Goes to the next page to parse
        nextPage_class = self.driver.find_element_by_css_selector('li[data-tl-object|=SR-PaginationNext] a.pagination--link')
        nextPage = nextPage_class.get_attribute("href")
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            self.page += 1
            yield response.follow(nextPage, callback=self.parse)

    def parse_house(self, house):

        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("------------------------New House--------------------------")
        print('On House: ' + str(self.i))
        print(house.url)
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        self.i += 1

        self.driver2.get(house.url)
        time.sleep(5)
        wait = WebDriverWait(self.driver2, 5)

        print("---------------------Getting Address Response-------------------------")
        address_response = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.address__label span.address__label-address')))
        area_response = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.address__label span.address__label-citystate')))
        address = [address_response.text, area_response.text]


        print("---------------------Getting Price Response-------------------------")
        listing_response =  wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'aside.property-info__details.details.font-size--m.sa-child.sa-child--3 ul')))
        listing_price = listing_response[0].text

        print("---------------------Getting SQFT Response-------------------------")
        sqft_response = listing_response[1].find_elements_by_css_selector('li')
        try:
            sqft = sqft_response[3].text
        except:
            sqft = sqft_response[2].text

        print("---------------------Getting Details Response-------------------------")
        try:
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.see-more__label.font-color--orange.sa-child.sa-child--3[data-tl-object = "Det-MoreHomeDetails"]')))
            button.click()
            print('Clicked the button')
        except:
            print('Didnt click the button')

        details_response = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.see-more__expandable section.home-details__list.list li')))
        details = []
        for detail in details_response:
            #detail_item = wait.until(EC.text_to_be_present_in_element((detail.find_elements_by_css_selector('span'))))
            detail_item = detail.find_elements_by_css_selector('span')
            det = []
            for item in detail_item:
                #print(item.text)
                det.append(item.text)
            details.append(det)


        print("---------------------Getting Pricing Response-------------------------")
        try:
            pricing_class = self.driver2.find_element_by_xpath('//*[@id="root"]/main/div[1]/section/div/div[1]/section[7]')
            button = pricing_class.find_element_by_css_selector('div.see-more__label.font-color--orange.sa-child.sa-child--3')
            button.click()
            clicked_button = True
            print('Clicked the button')
        except:
            clicked_button = False
            print('Didnt click the button')

        if not clicked_button:
            try:
                pricing_class = self.driver2.find_element_by_xpath('//*[@id="root"]/main/div[1]/section/div/div[1]/section[8]')
                button = pricing_class.find_element_by_css_selector('div.see-more__label.font-color--orange.sa-child.sa-child--3')
                button.click()
                print('Clicked the button')
            except:
                print('Didnt click the button')

        pricing_response = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section.price-history__list.list li')))
        pricing = []
        for price in pricing_response:
            price_table = price.find_elements_by_css_selector('span.label__inner-column')
            row = []
            for i in range(0,4):
                row.append(price_table[i].text)
            pricing.append(row)

        print("---------------------Getting Schools Response------------------")
        schools_response = self.driver2.find_elements_by_css_selector('section.schools__list.list li')

        schools = []
        for school in schools_response:
            school_name = school.find_element_by_css_selector('div.school-name').text
            school_distance = school.find_element_by_css_selector('span.school-distance strong').text
            schools.append([school_name, [school_distance]])


        yield{
            'address': address,
            'listing_price': listing_price,
            'sqft': sqft,
            'details': details,
            'pricing': pricing,
            'schools': schools,
            }
