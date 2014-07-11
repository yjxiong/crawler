# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 15:24:10 2014

@author: Xiong Yuanjun
"""

import csv, sys
import yaml
import logging

from pyYFCC100M import YFCCLoader

class YFCCCrawler():
    """The crawler class to load YFCC100M image"""

    def __init__(self, config_name):
        """Constructor for YFCCCrawler"""
        with open(config_name) as file:
            config = yaml.load(file)
        for f in config.keys():
            setattr(self, f, config[f])

    def get_loader_list(self):
        loader_list = [YFCCLoader(self.dataset_name_prefix, id) for id in self.crawl_numbers]
        return loader_list


crawler = YFCCCrawler('crawler_config.yaml')
