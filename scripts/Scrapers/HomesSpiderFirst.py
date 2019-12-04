import scrapy

class HomeListingSpider(scrapy.Spider):
    #Name of the craigslist spider
    name = "HomeListing"
    #Starting URL for Phoenix, AZ
    start_urls = ['https://www.homes.com/phoenix-az/homes-for-sale/']

    #Starting URL for Aurora, CO
    #start_urls = ['https://www.homes.com/aurora-co/homes-for-sale/']

    #Starting URL for Aurora, CO
    #start_urls = ['https://www.homes.com/riverside-ca/homes-for-sale/']

    def parse(self, response):
        print("---------------Response------------")
        print(response)

        #Creating the list of urls for each house link
        houses = response.css('div.card-wrapper.card-wrapper--property.grid-cell a::attr(href)').getall()
        print("---------------Houses------------")
        print(houses)
        for house in houses:
            #Calls the link of the house to parse
            yield response.follow(house, callback=self.parse_house)

        '''
        #Goes to the next page to parse
        nextPage = response.css('li[data-tl-object|=SR-PaginationNext] a.pagination--link::attr(href)').get()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)
        '''

    def parse_house(self, response):
        #location
        address_response = response.css('div.address__label')
        address = address_response[0].css('span::text').getall()

        #Pricing details
        listing_response = response.css('aside.property-info__details.details.font-size--m.sa-child.sa-child--3')
        listing_price = listing_response[0].css('strong::text').get()
        sqft = listing_response[1].css('li::text').getall()[2]

        #House Details
        details_response = response.css('div.see-more__expandable section.home-details__list.list li')
        details = []
        for detail in details_response:
            details.append(detail.css('span::text').getall())

        #Pricing history
        pricing_response = response.css('section.price-history__list.list li')
        pricing = []
        for price in pricing_response:
            pricing.append(price.css('span.label__inner-column::text').getall())

        #Schools Nearby
        schools_response = response.css('section.schools__list.list li')
        schools = []
        for school in schools_response:
            school_name = school.css('div.school-name::text').get()
            school_distance = school.css('span.school-distance strong::text').getall()
            schools.append([school_name, school_distance])

        yield{
            'address': address,
            'listing_price': listing_price,
            'sqft': sqft,
            'details': details,
            'pricing': pricing,
            'schools': schools,
            }
