import scrapy

class RealtorListingSpider(scrapy.Spider):
    #Name of the craigslist spider
    name = "RealtorListing"

    #Starting URL
    start_urls = ['https://www.realtor.com/realestateandhomes-search/Orange-County_CA']

    def parse(self, response):
        #Creating the list of urls for each house link
        houses = response.css('li.component_property-card.js-component_property-card.js-quick-view div.photo-wrap a::attr(href)').getall()


        for house in houses:
            #Calls the link of the house to parse
            yield response.follow(house, callback=self.parse_house)

        #Goes to the next page to parse
        nextPage = response.css('a.next::attr(href)').get()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            print(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)


    def parse_house(self, response):
        #Getting Attributes we care about
        address = response.css('div.ldp-header-address-wrapper.padding-bottom h1.display-inline span::text').getall()
        price = response.css('div.row.header-main-info.padding-bottom div.ldp-header-price-wrap.col-xxs-7.col-sm-12 span::attr(content)').get()
        beds = response.css('div.ldp-header-meta.mobile-wrapper.margin-bottom ul.property-meta.list-horizontal.list-style-disc.list-spaced li[data-label|=property-meta-beds] span::text').getall()

        baths =response.css('div.ldp-header-meta.mobile-wrapper.margin-bottom ul.property-meta.list-horizontal.list-style-disc.list-spaced li[data-label|=property-meta-bath] span::text').getall()
        if len(baths) == 0:
            baths =response.css('div.ldp-header-meta.mobile-wrapper.margin-bottom ul.property-meta.list-horizontal.list-style-disc.list-spaced li[data-label|=property-meta-baths] span::text').getall()

        sqft = response.css('div.ldp-header-meta.mobile-wrapper.margin-bottom ul.property-meta.list-horizontal.list-style-disc.list-spaced li[data-label|=property-meta-sqft] span::text').getall()
        lotsize = response.css('div.ldp-header-meta.mobile-wrapper.margin-bottom ul.property-meta.list-horizontal.list-style-disc.list-spaced li[data-label|=property-meta-lotsize] span::text').getall()

        #Creating a list of response objects for each feature
        features = response.css('div.page-content div.listing-section-details div.load-more-features.load-more-trigger div.row div.col-lg-3.col-sm-6.col-xs-6.col-xxs-12.ldp-features-image-tag.with-image')

        #Going through the list of features and saving to an array
        for feat in features:
            name = feat.css('h4::text').get()
            if name == 'Bedrooms':
                bedrooms = feat.css('li::text').getall()
            elif name == 'Bathrooms':
                bathrooms = feat.css('li::text').getall()
            elif name == 'Kitchen and Dining':
                kitchen = feat.css('li::text').getall()
            elif name == 'Exterior and Lot Features':
                exterior = feat.css('li::text').getall()


        #Storing all the random data about the house
        descriptions = response.css('div.page-content div.listing-section-details div.load-more-features.load-more-trigger div.row')
        data = []
        for i in range(1,len(descriptions)):
            data.append(descriptions[i].css('li::text').getall())

        #Historic Housing data
        historical_prices = response.css('div#ldp-history-price table.table td::text').getall()

        yield{
            'address': address,
            'price': price,
            'beds': beds,
            'baths': baths,
            'sqft': sqft,
            'lotsize': lotsize,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'kitchen': kitchen,
            'exterior':exterior,
            'random_data':data,
            'historical_prices':historical_prices
            }
