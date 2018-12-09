import os, fnmatch
import json
from pprint import pprint


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

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



for file in find('movies.json', '../categories/'):
	#print (file)
	with open(file ) as f:
		data = json.load(f)
		for x in data:
			#pprint(data[x]['movie_desc'])
			createMovieDescFile((str(file)).replace("movies.json","")+"moviesDescriptions/", str(x), str(data[x]['movie_desc']) )