import scrapy,random,string
from ..items import FlipkartElectronicsItem

class FlipkartSpider(scrapy.Spider):

    name = 'flipcamera'

    pageno=2

    start_urls=['https://www.flipkart.com/cameras/pr?sid=jek%2Cp31&otracker=categorytree&page=1']

    def parse(self, response):


        page = response.css("a._31qSD5::attr('href')").getall()

        for p in page:

            url = 'https://www.flipkart.com' + p


            yield scrapy.Request(url, callback=self.parse_elec)

        #accessing pages till 10th page
        page = 'https://www.flipkart.com/cameras/pr?sid=jek%2Cp31&otracker=categorytree&page=' + str(FlipkartSpider.pageno)
        if FlipkartSpider.pageno <= 10:
            FlipkartSpider.pageno += 1
            yield response.follow(page, callback=self.parse)


    def parse_elec(self, response):

                    items = FlipkartElectronicsItem()

                    product_name = response.xpath(
                        '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()').get()

                    spec_title = response.css(".col.col-3-12::text").extract()
                    spec_detail = response.css("._3YhLQA::text").extract()

                    storeprice = response.css('._3qQ9m1::text').extract()

                    storeLink = response.url

                    photos = response.css('div._2_AcLJ::attr(style)').extract()
                    l = photos[0].find("https")

                    k = storeLink.find("pid")

                    rating = response.css('.hGSR34::text').extract()

                    reviews = response.css('.qwjRop div div::text').extract()

                    product_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))

                    stores = {

                        "rating": "NA" if not rating else rating[0],
                        "reviews": reviews,
                        "storeProductId": storeLink[k + 4:k + 20],
                        "storeLink": storeLink,
                        "storeName": "Flipkart",
                        "storePrice": storeprice[0][1:]
                    }

                    items['product_name'] = product_name
                    items['product_id'] = product_id
                    items['stores'] = stores
                    items['category'] = 'electronics'
                    items['subcategory'] = 'camera'
                    items['brand'] = product_name.split()[0]
                    items['description'] = {}

                    for i in range(len(spec_title)):
                        items['description'][spec_title[i]] = spec_detail[i+1]

                    items["photos"] = photos[0][l:-1]


                    yield items