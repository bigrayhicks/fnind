
#!/usr/bin/python3
# mask-search-example
# what: this example searches up to different random terms plus the term you actually want to mask what you are searching for
# author: James Campbell
# date: 2015-12-12
# Note: MUST USE PYTHON 3 from terminal, e.g. python3 mask-search-example.py

import json
import urllib.request, urllib.parse
import random
import sys
sys.path.append('./assets')
from useragents import *

def searchG(searchfor):
    searchlist.append(searchfor)
    for terms in searchlist:
        randomuseragent = singlerando(useragents) # select a random user agent from list
        headers = { 'User-Agent' : randomuseragent } # get random header from above
        if terms != searchfor: # if the search term is not the one you care about, let the user know
            print ('This is a mask term: %s This is mask header: %s' % (terms,headers['User-Agent']))
        query = urllib.parse.urlencode({'q': terms})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query # GOOGLE ajax API string
        search_response_pre = urllib.request.Request(url,None,headers) # key to get the random headers to work
        search_response = urllib.request.urlopen(search_response_pre)
        search_results = search_response.read().decode("utf8")
        results = json.loads(search_results)
        data = results['responseData']
        if terms == searchfor:
            print('Total results: %s' % data['cursor']['estimatedResultCount'])
        hits = data['results']

        if terms == searchfor:
            print('Top %d hits:' % len(hits))
            for h in hits: print(' ', h['url'])
            print('For more results, see %s' % data['cursor']['moreResultsUrl'])
            resultdata = 0
            if len(hits > 0):
              resultdata = 1
        return resultdata

# global dictionary list of terms - do not change
diction = []
subset = []
lengthmin = 6
searchlist = [] # the list of terms that will be generated in the rando function
# randomly select the user agent for each search, make the useragents list as long as yout want ;)
fname = 'assets/dictionary-list.html'
with open(fname) as f:
    diction = f.readlines()
    for term in diction:
     if len(term) > lengthmin:
          subset.append(term.strip('\n'))

# function to get a random term or terms from the minlength dictionary in subset list
def rando(listofterms,num):
     i = 0
     while i < num:
          randomed = random.choice(listofterms)
          #print randomed
          searchlist.append(randomed)
          i = i + 1
     return # returning back searchlist appended with more results

# function that returns one random value from a list only
def singlerando(listofterms):
    randomed = random.choice(listofterms)
    return randomed


searchtype = int(input('Hello, are you searching by 1. domain, 2. email ?(# only): '))
rando(subset,searchtype) # get total list of terms based on numterms set in the globals section above
real_search = input('set search term: ') # set the search term
if (real_search == '')&(searchtype == 2):
  print('Since search input blank, example running as james@jamescampbell.us')
  real_search = 'james@jamescampbell.us'
elif (real_search == '')&(searchtype == 1):
  print('Since search blank, example running jamescampbell.us')
  real_search = 'jamescampbell.us'

gogetit = searchG(real_search)
if gogetit == 1:
  reportstyle = (input('You have results, would you like an html report? (y/n): '))
