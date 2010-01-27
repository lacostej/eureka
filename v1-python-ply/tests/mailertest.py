import mailer
import sys
from utils import *
import os

files = [ sys.argv[0] ]
other = "gen/pdfs/adeleide/adeleide.pdf"
if os.access(other, os.F_OK):
  files.append(other)

mailer.send_mail("eureka@vgsn.no", ["jerome.lacoste@gmail.com"], "Latest exercises from vgsn (7)", u(ur"Bla bla bla \u00f8 \u00d8"), files, "smtp.gmail.com", "jbhkb.eureka", "jVsmpdg1*")

