import logging
import requests
import csv
import StringIO


class YahooFinance(object):
    base_url = "http://finance.yahoo.com/d/quotes.csv"

    def get_quotes(self, symbols):
        resp = requests.get(self.base_url,
                            params={
                                "s": "+".join(symbols),
                                "f": "snl1c1mwvj1re",
                            })

        if not resp.ok:
            logging.error("Error getting quotes: %s", resp.text)
            return []

        reader = csv.DictReader(StringIO.StringIO(resp.text),
                                fieldnames=[
                                    "Symbol",
                                    "Name",
                                    "Price",
                                    "Change",
                                    "DaysRange",
                                    "52WeekRange",
                                    "Volume",
                                    "MarketCap",
                                    "P/E",
                                    "EPS"
                                ])

        quotes = [q for q in reader]
        return zip(symbols, quotes)
