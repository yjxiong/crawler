# -*- coding: utf-8 -*-
"""
File: test.py

Created on 2014/8/19 15:48

"""
__author__ = 'Xiong Yuanjun'


from crawler import YFCCCrawler

crawler = YFCCCrawler('crawler_config_video.yaml')

crawler.crawl(50)