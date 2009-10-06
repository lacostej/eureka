import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import mimetypes
import cStringIO
import base64
import email.Message
from tlslite.api import *
import quopri

def send_mail(send_from, send_to, subject, text, files=[], server="localhost", user=None, password=None):
  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )

  for fileName in files:
    contentType,ignored=mimetypes.guess_type(fileName)
    if contentType==None: # If no guess, use generic opaque type
      contentType="application/octet-stream"
    contentsEncoded=cStringIO.StringIO()
    f=open(fileName,"rb")
    mainType=contentType[:contentType.find("/")]
    if mainType=="text":
      cte="quoted-printable"
      quopri.encode(f,contentsEncoded,1) # 1 for encode tabs
    else:
      cte="base64"
      base64.encode(f,contentsEncoded)
    f.close()
    subMsg=email.Message.Message()
    subMsg.add_header("Content-type",contentType,name=fileName)
    subMsg.add_header("Content-transfer-encoding",cte)
    subMsg.set_payload(contentsEncoded.getvalue())
    contentsEncoded.close()
    msg.attach(subMsg)



#    part = MIMEBase('application', "octet-stream")
#    part.set_payload( open(file,"rb").read() )
#    Encoders.encode_base64(part)
#    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
#    msg.attach(part)

#  print server
  smtp = smtplib.SMTP(server, 587)
#  smtp.set_debuglevel(1)
  smtp.ehlo()
  settings = HandshakeSettings()
  smtp.starttls()
  if (user != None and password != None):
    smtp.login(user, password)
  print "Sending mail to " + msg['To']
  smtp.sendmail(send_from, send_to, msg.as_string())
  print "mail sent."
  smtp.close()
  print "done"

