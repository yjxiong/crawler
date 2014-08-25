# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 15:24:10 2014

@author: Xiong Yuanjun
"""

import csv
import yaml
import random
from multiprocessing.dummy import Pool
import urllib2
import requests
import re
from progressbar import *
import lmdb

from pyYFCC100M import YFCCLoader, YFCC_Item_TYPE

db_env = lmdb.Environment('./img_db/yfcc_img_db', map_size=2000000000000)

widgets = ['Progress: ', Percentage(), Bar(marker=RotatingMarker()),
                           ' ', ETA()]
pbar = ProgressBar(widgets=widgets)

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


def download_file_v2(link, id, prefix='../images/', retry=4, retry_base_time=1, do_download=False,
                     protobuf=None):

    if not do_download:
        return

    success = False

    for attempt in xrange(0, retry):

        r = requests.get(link, timeout=15, stream=False)

        ## Get file extension
        if 'content-disposition' in r.headers.keys():

            content_disposition = r.headers['content-disposition']
            parts = re.split('\.', content_disposition)
            file_extension = parts[-1]
        elif "." in link:
            parts = re.split('\.', link)
            file_extension = parts[-1]
        else:
            file_extension = '.jpg'

        ## composite file name
        file_name = '{:s}{:s}.{:s}'.format(prefix, id, file_extension)

        ## Download
        try:
            with open(file_name,'wb') as ofile:
                ofile.write(r.content)
        except:
            print 'download link %s fail, will retry later...'%link
            time.sleep(math.pow(2,attempt)*retry_base_time)
        else:
            success = True
            if protobuf:
                protobuf.item_data = r.content
            break
    else:
        print 'download link %s fail after %d retries, check connection.' %(link, retry)

    if success and protobuf:
        try:
            with db_env.begin(write=True) as txn:
                txn.put(id, protobuf.SerializeToString())
        except:
            print 'lmdb write failed.'



def download_callback(i):

    def _update(x):

        pbar.update(pbar.currval+1)

    return _update


class YFCCCrawler():
    """The crawler class to load YFCC100M image"""

    def __init__(self, config_name):
        """Constructor for YFCCCrawler"""
        with open(config_name) as file:
            config = yaml.load(file)
        for f in config.keys():
            setattr(self, f, config[f])

        self._mp_pool = Pool(int(self.mp_thread))

    def _get_loader_list(self):
        loader_list = [YFCCLoader(self.dataset_name_prefix, id) for id in self.crawl_numbers]
        return loader_list

    def crawl(self, max=None, perm=False, display=False, dump_to_txt=False):
        if max is None:
            crawl_num = self.crawl_number
        else:
            crawl_num = max

        loader_list = self._get_loader_list()

        pbar.maxval = crawl_num
        pbar.start()
        for i in xrange(crawl_num):
            if perm:
                loader = random.choice(loader_list)
                item = loader.next()

            else:
                for loader in loader_list:
                    if not loader.is_end:
                        break
                else:
                    raise StopIteration
                item = loader.next()

            if display:
                item.display()
            if dump_to_txt:
                dump_str = item.dump_text()
                dump_path = '{:s}{:s}.{:s}'.format(self.text_save_folder, item.id, 'txt')
                with open(dump_path,'w') as dump_file:
                    dump_file.write(dump_str)
            type_ = item.type
            prefix_ = self.image_save_folder if type_ == YFCC_Item_TYPE.Image else self.video_save_folder
            do_download = self.Download_image if type_ == YFCC_Item_TYPE.Image else self.Download_video
            self._mp_pool.apply_async(download_file_v2, args=(item.url, item.id),
                                      kwds ={'prefix':prefix_, 'retry':6, 'do_download': do_download,'protobuf':item.get_protobuf()},
                                      callback=download_callback(i))

        self._mp_pool.close()
        self._mp_pool.join()
        pbar.finish()

    def extract_video_list(self):

        with open('yfcc_video_dataset-0','wb') as csvout:
            writer = csv.writer(csvout, delimiter='\t')
            widgets = ['Reading files: ', Percentage(), Bar(marker=AnimatedMarker()),
                           ' ', ETA()]
            pbar_ = ProgressBar(widgets=widgets, maxval=10).start()
            counter = 0
            for loader in self._get_loader_list():

                while not loader.is_end:
                    item = loader.next()
                    if item is None:
                        continue
                    if item.type == YFCC_Item_TYPE.Video:
                        writer.writerow(item._raw)
                counter += 1
                pbar_.update(counter)
            pbar_.finish()




if __name__=='__main__':
    crawler = YFCCCrawler('crawler_config.yaml')

    # crawler.extract_video_list()
    crawler.crawl(10000,perm=False,dump_to_txt=True)
    # download_file(crawler._get_loader_list()[0].next()[1],'1.jpg')
    # crawler.get_video_file('video_url_list.csv')
    # print crawler._get_loader_list()[5].next().url
    # download_file_v2('http://farm8.staticflickr.com/7205/6985418911_df7747990d.jpg','123')