import sys
import json
import os,fnmatch
from pprint import pprint
from subprocess import call, check_output, Popen, PIPE
from urlparse import urlparse, parse_qsl

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
            


def getMoviesFromCategory(url, category):
    dic={}
    cmd ='scrapy runspider movie_list_scraper.py -a category=\"' +category  + '\" -s LOG_ENABLED=False -o ' + category + '.json'
    #process = Popen(cmd,shell=True, stdout=PIPE)
    pipes = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    std_out, std_err = pipes.communicate()
    pipes.wait()
    if pipes.returncode != 0:
        # an error happened!
        err_msg = "{}. Code: {}".format(std_err.decode("UTF-8"), pipes.returncode)
        print(err_msg)
    else:
        print("ok")

   

def getMovieInfo(real_url):
    cmd ='scrapy runspider movie_scraper.py -a url=\"' +real_url  + '\" -s LOG_ENABLED=False'
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
    process.wait()
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

def createMovieDescFile(folder_name,movie_name,movie_desc):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename=folder_name+ '/'+movie_name+'.txt'
    if os.path.exists(filename):
        return 
    else:
        append_write = 'w' # make a new file if not
    f = open(filename,append_write)
    f.write( movie_desc)
    f.close()


def function():
    for file in find('movies.json', '../categories/'):
        with open(file ) as f:
            data = json.load(f)
            for x in data:
                createMovieDescFile((str(file)).replace("movies.json","")+"moviesDescriptions/", str(x), str(data[x]['movie_desc']) )



def movieExists(movie_name):
    for file in find('*.txt', "../categories/"):
        real_name=(file.replace(".txt","").split("/")[-1])
        if real_name == movie_name:
            return True
    return False

        

def main(args):
    top_url = "https://www.imdb.com/chart/top"
    categories_dic = {}
    getCategories(top_url)
    for x in find('category_link.txt', '../categories/'):
        category = x.split("/")[2] 
        categories_dic[category]={}
        with open(x, 'r') as myfile:
            link=myfile.read().replace('\n', '')
            parse_url=  urlparse(link)
            query_dict = dict(parse_qsl(parse_url.query))
            category_url=query_dict['genres']
            getMoviesFromCategory(link,category_url)
            with open(category_url+'.json') as f:
                data = json.load(f)
            print ( "A categoria " + category +" tem " + str(len(data)) +" filmes")
            for key in data:
                if movieExists(key['title']):
                    print("Ja existe. Prooooximo!")
                    continue
                movie_dic = {}
                movie_dic['movie_title'] = key['title']
                real_movie_url=key['link'].replace("?ref_=adv_li_i","")
                print ("MOVIE = " + key['title'] )
                movie_desc = getMovieInfo("https://www.imdb.com"+real_movie_url)
                movie_dic['movie_desc'] = movie_desc
                #print (movie_desc)
                movie_parental_guide_url = real_movie_url +"parentalguide"
                parental_dic = getMovieParentalInfo(movie_parental_guide_url)
                movie_dic['movie_parental_guide'] = parental_dic
                categories_dic[category][key['title']] = movie_dic
                createMovieDescFile('../categories/'+ category +"/moviesDescriptions/", key['title'], movie_desc )
            with open('../categories/'+ category +'/movies.json', 'w') as outfile:
                json.dump(categories_dic[category], outfile)
            




if __name__ == "__main__":
   main(sys.argv[1:])


