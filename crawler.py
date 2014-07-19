# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 15:24:10 2014

@author: Xiong Yuanjun
"""

import csv, sys
import yaml
import logging
import random
from multiprocessing.pool import Pool
import urllib2
import time
import math

from pyYFCC100M import YFCCLoader



def download_file(link, file_name, retry=4, retry_base_time=1):

    for attempt in xrange(0, retry):

        try:
            data = urllib2.urlopen(link,timeout=15).read()
            with open(file_name,'wb') as ofile:
                ofile.write(data)
        except:
            print 'download link %s fail, will retry later...'%link
            time.sleep(math.pow(2,attempt)*retry_base_time)
        else:
            break
    else:
        print 'download link %s fail after %d retries, check connection.' %(link, retry)

class YFCCCrawler():
    """The crawler class to load YFCC100M image"""

    def __init__(self, config_name):
        """Constructor for YFCCCrawler"""
        with open(config_name) as file:
            config = yaml.load(file)
        for f in config.keys():
            setattr(self, f, config[f])

        self._mp_pool = Pool(256)

    def _get_loader_list(self):
        loader_list = [YFCCLoader(self.dataset_name_prefix, id) for id in self.crawl_numbers]
        return loader_list

    def crawl(self, max=None, perm=True):
        if max is None:
            crawl_num = self.crawl_number
        else:
            crawl_num = max

        loader_list = self._get_loader_list()


        for i in xrange(crawl_num):
            if perm:
                loader = random.choice(loader_list)
                image = loader.next()

            else:
                for loader in loader_list:
                    if not loader.is_end:
                        break
                else:
                    raise StopIteration
                image = loader.next()

            name = '../images/{:s}.jpg'.format(image.id)

            self._mp_pool.apply_async(download_file, args=(image.url, name))

        self._mp_pool.close()
        self._mp_pool.join()





if __name__=='__main__':
    crawler = YFCCCrawler('crawler_config.yaml')
    crawler.crawl(100000)
    # download_file(crawler._get_loader_list()[0].next()[1],'1.jpg')
