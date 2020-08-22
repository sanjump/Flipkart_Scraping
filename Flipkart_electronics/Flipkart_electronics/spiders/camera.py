import scrapy,random,string
from ..items import FlipkartElectronicsItem

class FlipkartSpider(scrapy.Spider):
    name = 'flipcamera'
    pageno=2
    start_urls=['https://www.flipkart.com/cameras/pr?sid=jek%2Cp31&otracker=categorytree&page=1']

    def parse(self, response):
                    items = FlipkartElectronicsItem()
                    all_div = response.css("div._3O0U0u")
                    for i in all_div:
                                product_name = i.css('div._3wU53n::text').get()
                                description = i.css('.tVe95H::text').extract()
                                storeprice = i.css('._2rQ-NK::text').extract()
                                storeLink = 'https://www.flipkart.com' + i.css("a._31qSD5::attr('href')").get()
                                photos = i.xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div/'
                                                 'div/div/a/div[1]/div[1]/div[1]/div/img').xpath("@src").get()
                                storeproductid=i.css("div::attr('data-id')").extract()
                                product_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))
                                stores = [{
                                    "storeProductId": storeproductid,
                                    "storeLink": storeLink,
                                    "storeName": "Flipkart",
                                    "storePrice": storeprice[0][1:]
                                }]


                                items['product_name'] = product_name
                                items['product_id'] = product_id
                                items['stores'] = stores
                                items['category'] = 'electronics'
                                items['subcategory'] = 'cameras'
                                items['description'] = description
                                items["photos"] = photos

                                yield items

                                next_page = 'https://www.flipkart.com/cameras/pr?sid=jek%2Cp31&otracker=categorytree&page=' + str(FlipkartSpider.pageno)
                                if FlipkartSpider.pageno<=15:
                                    FlipkartSpider.pageno +=1

                                    yield response.follow(next_page,callback=self.parse)
