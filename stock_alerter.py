import yaml
from lib.mailgun import MailGun
from lib.yql import YQL


ALERT_TEMPLATE = """Symbol: {Symbol}
Name: {Name}
Price: {LastTradePriceOnly}
Change: {Change}
Days Range: {DaysRange}
Year Low: {YearLow}
Year High: {YearHigh}
Market Cap: {MarketCapitalization}"""


class Alerter(object):

    def __init__(self, config):
        self.symbols = config["symbols"]
        self.from_addr = config["from-email"]
        self.to_addr = config["to-email"]
        self.yql = YQL()
        self.mailgun = MailGun(config["mailgun-domain"],
                               config["mailgun-api-key"])

    def check_alert(self, sym, quote):
        price = float(quote["LastTradePriceOnly"])
        low, high = self.symbols[sym]

        trigger = None
        if price <= low:
            trigger = "<= %.2f" % low
        elif price >= high:
            trigger = ">= %.2f" % high

        if trigger:
            subject = "Stock Alert: %s @ %.2f (%s)" % (sym, price, trigger)
            body = ALERT_TEMPLATE.format(**quote)
            self.mailgun.send_email(self.from_addr, self.to_addr, subject, body)

    def run(self):
        quotes = self.yql.get_quotes(self.symbols.keys())
        for sym, quote in quotes:
            self.check_alert(sym, quote)


if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.load(f)

    alerter = Alerter(config)
    alerter.run()
