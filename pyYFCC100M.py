# -*- coding: utf-8 -*-
"""
File: pyYFCC100M.py

Created on 2014/7/11 16:34

"""
__author__ = 'Xiong Yuanjun'

import yaml
import csv
import logging

class YFCCLoader():
    """
    The Loader for YFCC100M dataset
    """

    def _setup(self):
        with open('url_config.yaml') as config:
            self._config = yaml.load(config)
            self._line_tags = self._config['Fields']

    def __init__(self, name_prefix=None, id=None, input_file=None):
        """Constructor for YFCCLoader"""

        if input_file is None:
            input_file = open('{}-{:d}'.format(name_prefix,id))
            self._reader = csv.reader(input_file,delimiter='\t',
                        quoting=csv.QUOTE_NONE)

            # need to close
            self._need_close = True
            self._buffer = file
        else:
            self._need_close = False
        self._reader = csv.reader(input_file,delimiter='\t',
                        quoting=csv.QUOTE_NONE)

        self._pos = 0
        self._setup()


    def next(self):
        """
        Get next line
        :return:
        """
        ret = self._reader.next()
        self._pos+=1
        return ret

    @property
    def line_tags(self):
        try:
            return self._line_tags
        except AttributeError:
            logging.error('tags not loaded')
            return None

    @property
    def pos(self):
        return self._pos

    def clean_up(self):
        if self._need_close:
            self._buffer.close()

        # TODO add other clean up operation







