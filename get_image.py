#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from lxml import html
import re
import sys


def get_response(url,referer = "https://girl-atlas.com/album/58d15fcc92d302622dc57a80'",count = 1,timeout = 30):
    # 填充请求的头部
    print ("try %s url:%s") % (str(count),url)
    count += 1
    if count > 6 : return None
    headers = {
            # 'Host':"www.girls-altas.com",
            # "Content-type": "image/jpeg",
            # "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "referer":referer

    }
    try:
        return  requests.get(url, headers = headers,timeout = timeout)
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print "*" * 100
        return get_response(url,referer = referer,count = count,timeout = timeout)


def getAvUrl(str_class,url):
    start_url = 'https://girl-atlas.com'
    p1 = r"^/%s/.*" % str_class
    pattern1 = re.compile(p1)
    rst =  pattern1.findall(url)
    if len(rst) >= 1:
        return start_url + rst[0]

def getEncode(title):
    return title.encode("utf-8")

def get_tag_urls(url = 'https://girl-atlas.com/'):
    tag = []
    response = get_response(url)
    if response is  None:
        return None
    else:
        parsed_body = html.fromstring(response.text)
        next_url = parsed_body.xpath('//a/@href')
        tmp = ["tag" for i in range(0,len(next_url))]
        next_url = map(getAvUrl,tmp,next_url)
        next_url = [item for item in next_url if item is not None]
        tag.extend(next_url)
    # print next_url
    tag = list(set(tag))
    return tag


def get_album_urls(url = 'https://girl-atlas.com/'):
    #total 256 page album
    urls = [ url + "?p=%s" % (str(i)) for i in range(221,257) ]
    return urls


def get_page_urls(urls):
    album = []
    for url in urls:
        print url
        response = get_response(url)
        if response is  None:
            return None
        else:
            parsed_body = html.fromstring(response.text)
            next_url = parsed_body.xpath('//a/@href')
            tmp = ["album" for i in range(0,len(next_url))]
            next_url = map(getAvUrl,tmp,next_url)
            next_url = [item for item in next_url if item is not None]
            album.extend(next_url)
    # print next_url
    album = list(set(album))
    return album

# 获取每个girl专辑的Url
def get_girl_urls(page_urls):
    if page_urls is None:
        return None
    girl_urls = []

    count = 0
    start_dir = './data/'
    for url in page_urls:
        print url
        response = get_response(url)
        parsed_body = html.fromstring(response.text)
        # Xpath
        girl = parsed_body.xpath('/html/body/div[2]/section/div/div[1]/div[1]/ul/li/img/@src|/html/body/div[2]/section/div/div[1]/div[1]/ul/li/img/@delay')
        title = parsed_body.xpath('/html/body/div[2]/section/div/div[1]/div[1]/ul/li/img/@title')
        title = map(getEncode,title)
        tmp = zip(title, girl)
        pic = dict((x, y) for x, y in tmp)
        for k,v in pic.items():
            count += 1
            print count,k,v
            if "/" in k:k = k.replace("/","-")
            with open(start_dir + k + ".jpg", 'wb') as f:
                r = get_response(v)
                f.write(r.content)
            # with open("info.py","a") as f:
                # content = ("%s:%s\n") % (k,v)
                # f.writelines(content)
        girl_urls.append(pic)
    return girl_urls


# 开始下载图片
def get_images(girl_list):
    # 图片的默认存储文件夹
    if girl_list is None:
        return None
    count = 0
    start_dir = './data/'
    for pic in girl_list:
        for k,v in pic.items():
            count += 1
            print count,k,v
            with open(start_dir + k + ".jpg", 'wb') as f:
                r = get_response(v)
                f.write(r.content)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    start_time = time.time()
    print start_time
    ## download ablum url
    album_urls = get_album_urls()
    print album_urls
    page_urls = get_page_urls(album_urls)
    ## download tag url
    tag_urls = get_tag_urls()
    print tag_urls
    page_urls = get_page_urls(tag_urls)
    girl_urls = get_girl_urls(page_urls)
    stop_time = time.time()
    elapsed_time = time.time() - start_time
    print
    print "elasped %s seconds!!!!" % elapsed_time
