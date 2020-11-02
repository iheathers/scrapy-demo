import scrapy
from ..items import BookScraperItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    page = 2
    start_urls = [
        'https://www.amazon.com/Books-Last-30-days/s?rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page=1'
    ]

    def parse(self, response, **kwargs):
        items = BookScraperItem()

        books_div = response.css('div.a-section.a-spacing-medium')

        for book in books_div:
            title = book.css('.a-color-base.a-text-normal::text').get()
            author = book.css('.sg-col-12-of-28 .a-size-base+ .a-size-base::text').getall()
            price = book.css('.a-price-whole::text').getall()  # max of the list of prices in a book div
            image_url = book.css('.s-image::attr(src)').get()

            items['title'] = title
            items['author'] = author
            items['price'] = price
            items['image_url'] = image_url

            yield items

            next_page = f'https://www.amazon.com/Books-Last-30-days/s?rh=n%3A283155%2Cp_n_publication_date%3A1250226011&page={BooksSpider.page}'
            if BooksSpider.page <= 75:
                BooksSpider.page += 1
                yield response.follow(next_page, callback=self.parse)
