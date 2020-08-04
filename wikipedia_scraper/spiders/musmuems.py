import scrapy
import logging
import lxml.html


MUSUEM_LIST_XPATH = '/html/body/div[3]/div[3]/div[5]/div/table/tbody/tr/td[1]/a/@href'


class MusmuemsSpider(scrapy.Spider):
    name = 'musmuems'
    allowed_domains = ['wikipedia.com']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_most_visited_museums']
    collectable_attributes = ['Location', 'Collection size', 'Visitors']

    def parse(self, response):
        urls = response.xpath(MUSUEM_LIST_XPATH).extract()
        for url in urls:
            url = "https://en.wikipedia.com" + url
            print("FOLLOWING URL: {}".format(url))
            yield response.follow(url, callback=self.parse_musuem_metadata)

    def parse_musuem_metadata(self, response):
        meta_table = response.xpath('/html/body/div[3]/div[3]/div[5]/div/table[1]/*/tr').extract()
        if len(meta_table) < 1:
            logging.warning("Unexpected HTML received from url: {}".format(response.request.url))
            return

        meta_data = {'link': response.request.url}
        for data in meta_table:
            print(data)
            row = lxml.html.fromstring(data)
            if len(row.xpath("th")) < 1:
                continue

            if row.xpath("th")[0].text == 'Public transit access':
                meta_data['Public transit access count'] = len(row.xpath("td//a"))
                meta_data['Public transit access'] = row.xpath("td")[0].text_content()

            if row.xpath("th")[0].text in self.collectable_attributes:
                meta_data[row.xpath("th")[0].text] = row.xpath("td")[0].text_content()

        return meta_data
