#!/usr/bin/python3
# mask-search-example
# what: this searches emails, domains, etcetera
# author: James Campbell
# date: 2015-12-12
# Note: MUST USE PYTHON 3 from terminal, e.g. python3 mask-search-example.py

import json
import urllib.request, urllib.parse
import random
import sys
import os
import datetime
sys.path.append('./assets')
from useragents import *

# Global Variables
resultdata = 0
emailhuntapi = 'https://api.emailhunter.co/v1/'
authkey = 'bb0566a11bdf005001b919029deafb0d26a754d6' # replace with your own
domain = 'jamescampbell.us'
# Main Functions

# getToday gets the date
def getToday():
        return datetime.date.today().strftime("%Y%m%d")

# get email hunter api data

def emailhunt(searcheditem):
  randomuseragent = singlerando(useragents) # select a random user agent from list
  headers = { 'User-Agent' : randomuseragent } # get random header from above
  url = emailhuntapi+'search?domain='+searcheditem+'&api_key='+authkey # GOOGLE ajax API string
  print (url)
  search_response_e = urllib.request.Request(url,None,headers)
  search_response = urllib.request.urlopen(search_response_e)
  search_results = search_response.read().decode("utf8")
  resultse = json.loads(search_results)
  print (resultse)
  exit()


# htmlout spits out an html report with the results of the search
def htmlout(searcheditem,totalresults):
  outpath = os.path.expanduser('~')+'/'
  filename = "%s.%s" % (getToday(), "html")
  htmlfile = open(outpath+filename,'w+')
  htmlstr = '<!DOCTYPE HTML><head><title>report for' + searcheditem + '</title></head>'
  htmlstr = htmlstr + '''<body><div style="margin:10px;width:80%;font-family:monospace"><h2>Total Hits: '''+ totalresults + '''</h2>'''
  htmlfile.write(htmlstr)
  htmlfile.close()
  print('Report created in your home directory as %s' % filename)

# searchG searches Google using Google's API
def searchG(searchfor,resultdata=resultdata):
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
          totalhits = data['cursor']['estimatedResultCount']
          print('Total results: %s' % totalhits)
          hits = data['results']
          print('Top %d hits:' % len(hits))
          for h in hits: print(' ', h['url'])
          print('For more results, see %s' % data['cursor']['moreResultsUrl'])
          if int(totalhits) > 0:
            resultdata = 1
          return resultdata,totalhits

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
if gogetit[0] == 1:
  emailhunt(real_search)
  reportstyle = (input('You have results, would you like an html report? (y/n): '))
  if reportstyle == 'y':
    htmlout(real_search,gogetit[1])
  else:
    print('----------\nFnind Report Version 1.1\n\n----------\nTotal hits: %s\n' % (hits,))
    exit('Goodbye')
