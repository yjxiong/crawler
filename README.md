CRAWLER
=======

a simple python crawler for downloading YFCC100M dataset.


## Usage

```python

from crawler import YFCCCrawler

crawler = YFCCCrawler('crawler_config_video.yaml')

crawler.crawl(50, display=False)

```

This will download the first 50 videos.
