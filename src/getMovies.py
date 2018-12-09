import sys
import json
import os,fnmatch
from pprint import pprint
from subprocess import call, check_output, Popen, PIPE


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def getCategories(url):
        cmd ='scrapy runspider category_list_scraper.py -a url=' + url  + ' -s LOG_ENABLED=False'
        pipes = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        std_out, std_err = pipes.communicate()
        if pipes.returncode != 0:
            # an error happened!
            err_msg = "{}. Code: {}".format(std_err.decode("UTF-8"), pipes.returncode)
            print(err_msg)
        else:
            print("ok")
            


def getMoviesFromCategory(url):
    dic={}
    cmd ='scrapy runspider movie_list_scraper.py -a url=\"' +url  + '\" -s LOG_ENABLED=False'
    process = Popen(cmd,shell=True, stdout=PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            ss = output.strip().split("|")
            dic[ss[0]]=ss[1]
            #print ("title:"+ ss[0] + "||url:" + ss[1] )
    rc = process.poll()
    return dic

def getMovieInfo(title,url):
    cmd ='scrapy runspider movie_scraper.py -a url=\"' +url  + '\" -s LOG_ENABLED=False'
    process = Popen(cmd,shell=True, stdout=PIPE)
    desc=""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            desc= (output.strip()) #.split("|")
            #print ("title:"+ ss[0] + "||url:" + ss[1] )
    rc = process.poll()
    return desc

def getMovieParentalInfo(url):
    dic={}
    cmd ='scrapy runspider movie_parental_guide_scraper.py -a url=\"' +url  + '\" -s LOG_ENABLED=False'
    process = Popen(cmd,shell=True, stdout=PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            ss= output.strip().split("|")
            dic[ss[0]]=ss[1]
            #print ("title:"+ ss[0] + "||url:" + ss[1] )
    rc = process.poll()
    return dic


        

def main(args):
    top_url = "https://www.imdb.com/chart/top"
    categories_dic = {}
    getCategories(top_url)
    for x in find('category_link.txt', '../categories/'):
        category = x.split("/")[2] 
        categories_dic[category]={}
        with open(x, 'r') as myfile:
            link=myfile.read().replace('\n', '')
            dic =getMoviesFromCategory(link)
            for key in dic:
                movie_dic = {}
                movie_dic['movie_title'] = key
                real_movie_url=dic[key].replace("?ref_=adv_li_i","")
                movie_dic['movie_url'] = real_movie_url
                movie_desc = getMovieInfo(key,real_movie_url)
                movie_dic['movie_desc'] = movie_desc
                movie_parental_guide_url = real_movie_url +"parentalguide"
                parental_dic = getMovieParentalInfo(movie_parental_guide_url)
                movie_dic['movie_parental_guide'] = parental_dic
                categories_dic[category][key] = movie_dic
                print key
    
    for dicio in categories_dic:
        with open('../categories/'+ dicio +'/movies.json', 'w') as outfile:
            json.dump(categories_dic[categories_dic], outfile)




if __name__ == "__main__":
   main(sys.argv[1:])