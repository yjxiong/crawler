CRAWLER
=======

a simple python crawler for downloading YFCC100M dataset.


## Usage

The config file `crawler_config_video.yaml` has following fields:

```

crawl_number: 2000 #number of images to crawl

dataset_name_prefix: ../link/yfcc_video_dataset

video_save_folder: ../videos/

image_save_folder: ../images/

text_save_folder: ../des/

crawl_numbers: # id list of url link file, range 0-9, you can specify multiple link files here
  - 0

```

You can set the place for saving the videos and images by setting `video_save_folder` and `image_save_folder`.

`text_save_folder` configures the place for saving text descritionps. Every image/video has a txt file in json format. It contains title, description, user tags and machine tags.

You can either set the number of items to crawl in the config file or by method argument.

Put the link file in `/link/` and run:

```Python

from crawler import YFCCCrawler

crawler = YFCCCrawler('crawler_config_video.yaml')

crawler.crawl(50)

```

This will download the first 50 videos.

In case you run into dependency issues, run in terminal
 
```
pip install -r requirements.txt
```
