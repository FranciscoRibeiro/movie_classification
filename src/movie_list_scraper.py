# -*- coding: utf-8 -*-
import os
import scrapy

# https://www.imdb.com/search/title?genres=adventure&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=62P1QRR4290AGXBH0DW7&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_2

class MovieListSpider(scrapy.Spider):
    name = 'https://www.imdb.com'

    def start_requests(self):
        url = ''
        tag = getattr(self, 'url', None)
        if tag is not None:
            url = tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        movies_list_wrapper = response.xpath('//div[@id="main"]')
        for anode in movies_list_wrapper.css('div.article div.list div.lister-item'):
            #link = anode.css('a::attr(href)').extract_first()
            #category= anode.xpath('a/text()')
            link = anode.css('div.lister-item-image a::attr(href)').extract_first()
            title = anode.css('div.lister-item-image img::attr(alt)').extract_first()
            print (title +"|" +self.name+ link)
            #createCategoryAndFile('categories/'+ letters(str(category.extract_first())), self.name +link)


def letters(input):
    return ''.join(filter(str.isalpha, input))

def createCategoryAndFile(category_name,link):
    if not os.path.exists(category_name):
        os.makedirs(category_name)
    filename=category_name+ '/category_link.txt'
    if os.path.exists(filename):
        return 
    else:
        append_write = 'w' # make a new file if not
    f = open(filename,append_write)
    f.write( link)
    f.close()
