from bithumb_notice_crawler import BithumbNoticeCrawler

crawler = BithumbNoticeCrawler()

while True:
    res = crawler.detect_new_notice()
    print(res)
    if res['status'] == 'detected':
        new_notice = res['notice']



