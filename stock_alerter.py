import urllib2
import simplejson
import yaml

with open("config.yml", "r") as f:
    config = yaml.load(f)

ENV = "store://datatables.org/alltableswithkeys"
BASE_URL = "http://query.yahooapis.com/v1/public/yql?q=%s&format=json&env=%s"


def build_query(symbols):
    q = ",".join("'%s'" % s for s in symbols)
    return "select * from yahoo.finance.quote where symbol in (%s)" % q

def get_prices(symbols):
    query = build_query(symbols)
    url = BASE_URL % (urllib2.quote(query), urllib2.quote(ENV))
    response = urllib2.urlopen(url)
    json = simplejson.loads(response.read())
    results = json["query"]["results"]["quote"]
    prices = [r["LastTradePriceOnly"] for r in results]
    return zip(symbols, prices)


if __name__ == "__main__":
    print get_prices(config["symbols"])
