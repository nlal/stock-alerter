import traceback
import yaml
from datetime import datetime, timedelta
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

    def __init__(self, config, last_triggered):
        self.symbols = config["symbols"]
        self.from_addr = config["from-email"]
        self.to_addr = config["to-email"]
        self.yql = YQL()
        self.mailgun = MailGun(config["mailgun-domain"],
                               config["mailgun-api-key"])
        self.last_triggered = last_triggered

    def check_alert(self, sym, quote):
        now = datetime.now()
        if now <= self.last_triggered.get(sym, datetime.min) + timedelta(days=1):
            return

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
            self.last_triggered[sym] = now

    def run(self):
        try:
            quotes = self.yql.get_quotes(self.symbols.keys())
            for sym, quote in quotes:
                self.check_alert(sym, quote)
        except Exception as e:
            subject = "Stock Alert Error: %s" % str(e)
            body = traceback.format_exc()
            self.mailgun.send_email(self.from_addr, self.to_addr, subject, body)


if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.load(f)

    with open("last-triggered.yml", "r+") as f:
        last_triggered = yaml.load(f) or {}

        alerter = Alerter(config, last_triggered)
        alerter.run()

        f.seek(0)
        yaml.dump(last_triggered, f, default_flow_style=False)
