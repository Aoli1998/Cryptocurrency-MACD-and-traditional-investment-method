import feapder
import time
import json
import csv


class SpiderTest(feapder.AirSpider):
    def start_requests(self):
        time_stamp = int(time.time())
        yield feapder.Request(f"https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug=bitcoin&time_end={time_stamp}&time_start=1367107200")

    def bs4(self, features="html.parser"):
        pass

    def parse(self, request, response):
        #article_list = response.xpath('//a[@class="recmd-content"]')  #这里可以用bs4
        article_list = response.content
        content = json.loads(article_list)
        quoteList = content['data']['quotes']
        print(quoteList)
        with open('BTC.csv', 'w', encoding='utf8', newline='') as f:
            csv_write = csv.writer(f)
            csv_head = ["Date", "open", "high", "close", "low", "Volume"]
            csv_write.writerow(csv_head)

            for quote in quoteList:
                quote_date = quote["time_open"][:10]
                quote_open = "{:.2f}".format(quote["quote"]["USD"]["open"])
                quote_high = "{:.2f}".format(quote["quote"]["USD"]["high"])
                quote_close = "{:.2f}".format(quote["quote"]["USD"]["close"])
                quote_low = "{:.2f}".format(quote["quote"]["USD"]["low"])
                quote_volume = "{:.2f}".format(quote["quote"]["USD"]["volume"])
                csv_write.writerow([quote_date, quote_open, quote_high, quote_close, quote_low, quote_volume])

        print("Done")



    def parse_detail(self, request, response):
        """
        解析详情
        """
        # 取url
        url = request.url
        # 取title
        title = request.title
        # 解析正文
        content = response.xpath(
            'string(//div[@class="content"])'
        ).extract_first()  # string 表达式是取某个标签下的文本，包括子标签文本

        print("url", url)
        print("title", title)
        print("content", content)


if __name__ == "__main__":

    SpiderTest().start()