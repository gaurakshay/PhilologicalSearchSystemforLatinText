#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


header_size_count = 0
response_size_count = 0
link = 'http://www.thelatinlibrary.com/mirandola.html'
# Create request and add header so that 
# requests to fetch data are identifiable.
request = urllib2.Request(link)
request.add_header("User-Agent", \
        "Gallogly College of Engineering - University of Oklahoma, \
        Class - Intro to Text Analytics")
print ("opening url: " + link)
response = urllib2.urlopen(request)
header   = response.info()
url      = response.geturl()
code     = response.getcode()
header_size_count += int(header.getheaders("Content-Length")[0])

html_file_content = response.read()
response_size_count += len(html_file_content)
#file_cont    = response.readlines()
#print (type(html_file_content))
#print (type(file_cont))

html_soup = BeautifulSoup(html_file_content, 'html.parser')
#print (html_soup.prettify())

# Get the title of the page
print html_soup.title.string.strip()

# Find tag that has class "pagehead" and get its text
print html_soup.find(class_="pagehead").get_text()

for link in html_soup.find_all('a'):
    print link.get('href')


print "Header size be like: %d " %  header_size_count
print "Response size be like: %d " %  response_size_count

def test_check_size():
    print (header_size_count)
    print (response_size_count)
    assert header_size_count == response_size_count

#print
#print
#print header
#print
#print
#print url
#print
#print
#print code
#print
#print
#print site
#site_data = site.readlines()
#print
#print
#print site_data
