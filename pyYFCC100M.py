# -*- coding: utf-8 -*-
"""
File: pyYFCC100M.py

Created on 2014/7/11 16:34

"""
__author__ = 'Xiong Yuanjun'

import yaml
import csv
import logging
import pprint
import urllib
import json
from enum import Enum
import yfcc100m_pb2
import json

class YFCC_Item_TYPE(Enum):
    Image = 1
    Video = 2

class YFCCItem():

    def __init__(self, id_, url_, name_, display_=None, raw=None, type_=YFCC_Item_TYPE.Image):
        self._item_id = id_
        self._item_url = url_
        self._item_name = name_
        self._display_list = display_
        self._raw = raw
        self._item_type = type_

    @property
    def url(self):
        return self._item_url

    @property
    def name(self):
        return self._item_name

    @property
    def id(self):
        return self._item_id

    @property
    def type(self):
        return self._item_type

    def display(self):
        pprint.pprint(self._display_list)

    def dump_text(self):
        return json.dumps(self._display_list)

    def get_protobuf(self):
        msg = yfcc100m_pb2.ItemBlob()
        msg.item_id = self._item_id
        msg.item_raw_info = json.dumps(self._raw)
        msg.item_display_list = json.dumps(self._display_list)
        msg.item_type = yfcc100m_pb2.ItemBlob.IMAGE if self._item_type == YFCC_Item_TYPE.Image \
            else yfcc100m_pb2.ItemBlob.VIDEO
        return msg


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
            self._type_marker = self._line_tags.index(self._config['type_marker'])
            self._display_fields = [self._line_tags.index(x) for x in self._config['display']]


    def __init__(self, name_prefix=None, id=None, input_file=None):
        """Constructor for YFCCLoader"""

        csv.field_size_limit(1000000000)
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
        self.input_file = input_file


    def next(self):
        """
        Get next line
        :return:
        """
        if self._end:
            return None
        try:
            ret = self._reader.next()
            self._pos += 1
            type_ = YFCC_Item_TYPE.Image if ret[self._type_marker] == "0" else YFCC_Item_TYPE.Video

        except StopIteration:
            self._end=True
            return None

        return YFCCItem(ret[self._id_tag_idx], ret[self._url_tag_idx], '',
                        type_=type_,
                        display_={name: urllib.unquote(ret[x]).decode('utf8') for name, x in zip(self._config['display'], self._display_fields)},
                        raw=ret)

    def get_list(self):
        yield self.next()


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







