import csv
from mail import *
from app import *

mails = []
data_to_append = []

file = open('mails.csv', 'a', newline = '')
writer = csv.writer(file)

for i in range(len(ids)):
    x = server.mail(server.listids()[i])
    mail = []
    mail.append(x.date)
    mail.append(x.title)
    mail.append(x.from_addr)
    mail.append(x.body)
    data_to_append.append(mail)

    print(type(x))
    print(type(x.body))
# data_to_append.append(mails)
writer.writerows(data_to_append)

file.close()
