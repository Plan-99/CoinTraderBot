import requests
import time
from bs4 import BeautifulSoup


class BithumbNoticeCrawler:
    def __init__(self):
        self.last_notice = self.get_last_notice()['notice']

    def get_last_notice(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://www.google.co.uk/',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1'
        }
        url = 'https://feed.bithumb.com/notice'
        now = time.localtime()
        now = time.strftime('%Y-%m-%d %H:%M:%S', now)
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            notices = soup.select('a[href*="/notice/"]')
            for notice in notices:
                class_list = notice.get('class')
                for class_ in class_list:
                    if 'fixed' in class_:
                        break
                else:
                    texts = notice.select('span')
                    title = texts[0].text
                    link = notice.get('href')
                    notice_id = link.replace('/notice/', '')
                    return {
                        'status': 'succeed',
                        'notice': {
                            'title': title,
                            'id': notice_id,
                            'timestamp': now,
                        }
                    }
        except Exception as e:
            return {
                'status': 'failed',
                'message': f"Error occurred while getting Bithumb Notice from mobile: {e} ({now})",
            }

    def detect_new_notice(self):
        res = self.get_last_notice()
        if res['status'] == 'failed':
            return res
        last_notice_from_bithumb = res['notice']
        if last_notice_from_bithumb['id'] != self.last_notice['id']:
            self.last_notice = last_notice_from_bithumb
            return {
                'status': 'detected',
                'notice': self.last_notice
            }
        else:
            return {
                'status': 'non-detected',
            }
