import easyimap as e
# import pprint

user = "mails.test07@gmail.com"
password = "leidgincvhuqdwtf"

server = e.connect("imap.gmail.com", user, password)

ids = server.listids()

email = server.mail(server.listids()[0])
mails = []

for i in range(len(ids)):
    x = server.mail(server.listids()[i])
    mails.append(x.body)

# pprint.pprint(mails)

