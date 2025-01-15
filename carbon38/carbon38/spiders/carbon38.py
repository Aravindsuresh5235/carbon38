import scrapy


class Carbon38(scrapy.Spider):
    name = "carbon38"
    start_urls = ['https://www.carbon38.com/shop-all-activewear/tops']

    def parse(self, response):
        try:
            for links in response.css('a.ProductItem__ImageWrapper::attr(href)'):
                yield response.follow(links.get(), callback=self.parse_products)

            next_page = response.css('a.Pagination__NavItem[rel="next"]::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
        except Exception as e:
            self.logger.error(f"Error in parse: {e}")

    def parse_products(self, response):
        try:
            yield {
                "breadcrumbs": None, 

                "primary_image_url": "https:" + response.css('div.AspectRatio img::attr(src)').get(),

                "brand": response.css('h2.ProductMeta__Vendor.Heading.u-h1 a::text').get(),

                "product_name": response.xpath('//h1[@class="ProductMeta__Title Heading u-h3"]/text()').get(),

                "price": response.css('span.ProductMeta__Price.Price::text').get(),

                "reviews": response.css('div.yotpo-sr-bottom-line-text--right-panel.yotpo-sr-bottom-line-text').get(),

                "color": response.css('span.ProductForm__SelectedValue::text').get(),

                "sizes": response.css('ul.SizeSwatchList li.HorizontalList__Item label.SizeSwatch::text').getall(),

                "description": response.css('div.Faq_AnswerWrapper div.Faq_Answer p::text').get(),

                "sku": None,

                "product_id": None,

                "product_url": response.xpath('//link[@rel="canonical"]/@href').get(),
                
                "image_urls": ["https:" + url for url in response.css('div.AspectRatio img::attr(src)').getall()],
            }
        except Exception as e:
            self.logger.error(f"Error in parse_products: {e}")