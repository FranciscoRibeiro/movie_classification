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
        dic = {}
        secs = response.css('section.article section')
        for section in secs:
            tab= section.css('h4.ipl-list-title::text')
            degree=section.css('li.advisory-severity-vote span.ipl-status-pill::text')
            #print( str(tab.extract_first()) + " | " + str(degree.extract_first()))
            key= str(tab.extract_first())
            value = str(degree.extract_first())
            if letters(key) in dic:
                if value != 'None' and value!= None :
                    dic[letters(key)]= value
            else:
                dic[letters(key)]= value
        for x in dic:
            print(x+"|"+dic[x])


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
