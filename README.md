CRAWLER
=======

a simple python crawler for downloading YFCC100M dataset.


## Usage

The config file `crawler_config_video.yaml` has following fields:

```

# Configuration of the crawler

config_name: YFCC100M_0_VIDEO

crawl_number: 2000 #number of images to crawl

crawl_order: seq # can use seq, rand, ..

use_mp: True # switch for whether use multiprocessing
mp_thread: 32

dataset_name_prefix: ../link/yfcc_video_dataset

video_save_folder: ../videos/

image_save_folder: ../images/

crawl_numbers: # id list of url link file, range 0-9, you can specify multiple link files here
  - 0

```

You can set the place for saving the videos and images by setting `video_save_folder` and `image_save_folder`.

You can either set the number of items to crawl in the config file or by method argument.

```python

from crawler import YFCCCrawler

crawler = YFCCCrawler('crawler_config_video.yaml')

crawler.crawl(50, display=False)

```

This will download the first 50 videos.
