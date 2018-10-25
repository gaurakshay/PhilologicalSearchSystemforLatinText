#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program to download Mirandola text."""

# Import required packages
import urllib2
from bs4 import BeautifulSoup
import re
import json
import codecs

# Variables to keep track of response size in header
# and the actual data read.
header_response_size = 0
read_response_size = 0
# Create object to store all the data of the author
mirandola_json = {}


def get_html_data(link):
    """Get the data from the link."""
    global header_response_size
    global read_response_size
    # Create a request and add header to make it easier for site
    # admin to identify who/what the pull request is for
    request = urllib2.Request(link)
    request.add_header("User-Agent",
                       "CS 5970-995 Intro to Text Analytics,\
                       Gallogly College of Engineering,\
                       University of Oklahoma")
    response = urllib2.urlopen(request)
    # Update header response size and read response size if the
    # page request was successful.
    if (response.getcode() == 200):
        header_response_size += int(response
                                    .info()
                                    .getheaders('Content-Length')[0])
        temp = response.read().decode('utf-8')
        read_response_size += len(temp)
        response.close()
        return temp
    else:
        print ('Couldn\'t reach the link: %s' % link)
        response.close()


def update_chapter_details(link, html):
    chapters = []
    chapter = {}
    verses = []
    header_tag = html.find(class_='pagehead')
    chapter_name = header_tag.get_text(" ", strip=True)
    #print (type(chapter_name))
    chapter.update({u'chapter' : chapter_name})
    if(re.compile('oratio').search(link)):
        p_tags = html.find_all('p', class_="")
        i = 1
        for tag in p_tags:
            if(tag.table or tag.b):
                pass
            else:
                verse = {}
                verse.update({u'verse' : i})
                passage = ' '.join(tag.get_text(strip=True).split())
                passage = re.sub(r'[0-9]{1,4}\.\s', '', passage)
                verse.update({u'passage' : passage})
                verse.update({u'link' : link})
                verses.append(verse)
                i += 1
    else:
        data_tag = (header_tag
                    .next_sibling
                    .next_sibling
                    .next_sibling
                    .next_sibling)
        i = 1
        for line in data_tag.get_text().splitlines(True):
            if(len(line)>1):
                verse = {}
                verse.update({u'verse' : i})
                verse.update({u'passage' : ' '.join(line.split())})
                verse.update({u'link' : link})
                verses.append(verse)
                i += 1
    chapter.update({u'verses' : verses})
    chapters.append(chapter)
    return chapters


def update_book_details(base_url, html):
    booknames = []
    """Get child links from html passed"""
    # Find child links with mirandola in them.
    child_links = html.find_all(href=re.compile('mirandola'))
    booknames = []
    for link in child_links:
        child_url = link.get('href')
        child_data = BeautifulSoup(get_html_data(base_url + 
                                                 child_url),
                                   'html.parser')
        chapters = update_chapter_details(base_url + child_url
                                          , child_data)
        book = {}
        book.update({u'bookname' : link.get_text(strip=True)})
        book.update({u'chapters' : chapters})
        booknames.append(book)
    mirandola_json.update({u'books' : booknames})
    #print (json.dumps(mirandola_json, indent=4,
    #                  separators=(',',': '),
    #                  ensure_ascii=False)).encode('utf-8')


def test_mirandola_download():
    """Test correctness of download."""
    print
    base_url = 'http://www.thelatinlibrary.com/'
    author_url = 'mirandola.html'
    html_data = BeautifulSoup(get_html_data(base_url + 
                                            author_url),
                              'html.parser')
    author_tag = html_data.find(class_='pagehead')
    author_tag_txt = (author_tag.get_text(" ", strip=True))
    author_name = ' '.join(re.findall(r'[a-zA-Z]+', author_tag_txt))
    date_ = (' '.join(re.findall(r'\([\s\S]+\)', author_tag_txt)))[1:-1]
    title = (author_tag.next_sibling.next_sibling.next_sibling
             .next_sibling.find('td').get_text(' ', strip=True))
    mirandola_json.update({u'author_name' : author_name})
    mirandola_json.update({u'title' : re.sub(r'.html', '', author_url)})
    mirandola_json.update({u'dates' : date_})
    mirandola_json.update({u'language' : u'latin'})
    update_book_details(base_url, html_data)
    with codecs.open('mirandola.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(mirandola_json, indent=4,
                           separators=(',', ': '),
                           ensure_ascii=False))

    print ('Size of download ' + str(header_response_size) + 'B')
    assert header_response_size == read_response_size
