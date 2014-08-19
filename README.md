CRAWLER
=======

a simple python crawler for downloading YFCC100M dataset.


## Usage

Put the code in a folder `crawler`. In the upper directory create a folder named `videos`.

```python

from crawler import YFCCCrawler

crawler = YFCCCrawler('crawler_config_video.yaml')

crawler.crawl(50, display=False)

```

This will download the first 50 videos.
