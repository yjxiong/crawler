# -*- coding: utf-8 -*-
"""
File: pyYFCC100M.py

Created on 2014/7/11 16:34

"""
__author__ = 'Xiong Yuanjun'

import yaml
import csv
import logging

class YFCCImage():

    def __init__(self, id_, url_, name_):
        self._image_id = id_
        self._image_url = url_
        self._image_name = name_

    @property
    def url(self):
        return self._image_url

    @property
    def name(self):
        return self._image_name

    @property
    def id(self):
        return self._image_id

class YFCCLoader():
    """
    The Loader for YFCC100M dataset
    """

    def _setup(self):
        with open('url_config.yaml') as config:
            self._config = yaml.load(config)
            self._line_tags = self._config['Fields']
            self._url_tag_idx = self._line_tags.index(self._config['download_tag'])
            self._id_tag_idx = self._line_tags.index(self._config['id_tag'])


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
        self._end=False


    def next(self):
        """
        Get next line
        :return:
        """
        if self._end:
            return None
        try:
            ret = self._reader.next()
            self._pos+=1
        except StopIteration:
            self._end=True
            return None,None
        # return ret, ret[self._url_tag_idx], ret[self._id_tag_idx]
        return YFCCImage(ret[self._id_tag_idx], ret[self._url_tag_idx], '')


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

    @property
    def is_end(self):
        return self._end

    def clean_up(self):
        if self._need_close:
            self._buffer.close()

        # TODO add other clean up operation







