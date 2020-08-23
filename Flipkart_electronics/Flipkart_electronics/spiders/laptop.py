import scrapy,random,string
from ..items import FlipkartElectronicsItem

class FlipkartSpider(scrapy.Spider):
    name = 'fliplaptop'
    pageno=2
    start_urls=['https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&page=1']


    def parse(self, response):

        page = response.css("a._31qSD5::attr('href')").getall()
        for p in page:
            url = 'https://www.flipkart.com' + p
            yield scrapy.Request(url, callback=self.parse_elec)

        page = 'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&page=' + str(FlipkartSpider.pageno)
        if FlipkartSpider.pageno <= 10:
            FlipkartSpider.pageno += 1
            yield response.follow(page, callback=self.parse)

    def parse_elec(self, response):

                        items = FlipkartElectronicsItem()
                        product_name = response.xpath(
                            '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()').get()
                        description = response.css('._2-riNZ::text').extract()
                        storeprice = response.css('._3qQ9m1::text').extract()
                        storeLink = response.url
                        photos = response.xpath(
                            '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/img').xpath(
                            "@src").get()
                        k = storeLink.find("pid")
                        rating = response.css('.hGSR34::text').extract()
                        reviews = response.css('.qwjRop div div::text').extract()
                        product_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))
                        stores = [{
                            "storeProductId": storeLink[k + 4:k + 20],
                            "storeLink": storeLink,
                            "storeName": "Flipkart",
                            "storePrice": storeprice[0][1:]
                        }]

                        items['product_name'] = product_name
                        items['product_id'] = product_id
                        items['stores'] = stores
                        items['category'] = 'electronics'
                        items['subcategory'] = 'speakers'
                        items['description'] = description
                        items["photos"] = photos
                        items["rating"] = rating[0]
                        items['reviews'] = reviews

                        yield items
