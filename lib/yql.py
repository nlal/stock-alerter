import logging
import requests

class YQL(object):
    base_url = "http://query.yahooapis.com/v1/public/yql"
    quotes_query = "select * from yahoo.finance.quote where symbol in (%s)"
    env = "store://datatables.org/alltableswithkeys"

    def get_quotes(self, symbols):
        query = self.quotes_query % ",".join("'%s'" % s for s in symbols)
        resp = requests.get(self.base_url,
                            params={
                                "q": query,
                                "env": self.env,
                                "format": "json",
                            })
        if not resp.ok:
            logging.error("Error getting quotes: %s", resp.text())
            return []

        quotes = resp.json()["query"]["results"]["quote"]
        if not isinstance(quotes, list):
            quotes = [quotes]

        return zip(symbols, quotes)
