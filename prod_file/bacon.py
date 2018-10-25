#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program to download Bacon text."""

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
bacon_json = {}


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
        temp = response.read().decode('utf-8', 'replace')
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
    chapter.update({u'chapter': chapter_name})
    data_tag = (html.find_all('p', class_=''))
    i = 1
    for tag in data_tag:
        if (tag.table):
            continue
        verse = {}
        verse.update({u'verse': i})
        verse.update({u'passage': ' '.join(tag.get_text(' ', strip=True)
                                           .split())})
        verse.update({u'link': link})
        verses.append(verse)
        i += 1
    chapter.update({u'verses': verses})
    chapters.append(chapter)
    return chapters


def update_book_details(base_url, html):
    booknames = []
    """Get child links from html passed"""
    # Find child links with bacon in them.
    child_links = html.find_all(href=re.compile('bacon'))
    booknames = []
    for link in child_links:
        child_url = link.get('href')
        child_data = BeautifulSoup(get_html_data(base_url +
                                                 child_url),
                                   'html.parser')
        chapters = update_chapter_details(base_url + child_url, child_data)
        book = {}
        book.update({u'bookname': link.get_text(strip=True)})
        book.update({u'chapters': chapters})
        booknames.append(book)
    bacon_json.update({u'books': booknames})
    print (json.dumps(bacon_json, indent=4,
                      separators=(',', ': '),
                      ensure_ascii=False)).encode('utf-8')


def test_bacon_download():
    """Test correctness of download."""
    print
    base_url = 'http://www.thelatinlibrary.com/'
    author_url = 'bacon.html'
    html_data = BeautifulSoup(get_html_data(base_url +
                                            author_url),
                              'html.parser')
    author_tag = html_data.find(class_='pagehead')
    author_tag_txt = (author_tag.get_text(" ", strip=True))
    author_name = ' '.join(re.findall(r'[A-Z]+', author_tag_txt))
    date_ = (' '.join(re.findall(r'\([\s\S]+\)', author_tag_txt)))[1:-1]
    bacon_json.update({u'author_name': author_name})
    bacon_json.update({u'title': re.sub(r'.html', '', author_url)})
    bacon_json.update({u'dates': date_})
    bacon_json.update({u'language': u'latin'})
    update_book_details(base_url, html_data)
    #with codecs.open('bacon.txt', 'w', encoding='utf-8') as f:
    #    f.write(json.dumps(bacon_json, indent=4,
    #                       separators=(',', ': '),
    #                       ensure_ascii=False))

    print ('Size of download ' + str(header_response_size) + 'B')
    assert header_response_size == read_response_size
