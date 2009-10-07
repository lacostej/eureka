import mailer
import sys
from utils import *

f = sys.argv[0]
mailer.send_mail("eureka@vgsn.no", ["jerome.lacoste@gmail.com"], "Latest exercises from vgsn (7)", u(ur"Bla bla bla \u00f8 \u00d8"), [f], "smtp.gmail.com", "jbhkb.eureka", "jVsmpdg1*")
