import mailer
import sys

f = sys.argv[0]
mailer.send_mail("eureka@vgsn.no", ["jerome.lacoste@gmail.com"], "Latest exercises from vgsn", "Bla bla bla", [f], "smtp.gmail.com", "jbhkb.eureka", "jVsmpdg1*")
