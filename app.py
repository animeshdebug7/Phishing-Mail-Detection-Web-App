from flask import Flask
from flask import render_template, redirect, request
from transformers import BertConfig, BertModel, TFDistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast
from transformers import TextClassificationPipeline
from transformers import DistilBertTokenizerFast
import csv
import easyimap as e


user = "*"
password = "#"

server = e.connect("imap.gmail.com", user, password)
# email = server.mail(server.listids())
mails = []

# for i in range(len(ids)):
#     x = server.mail(server.listids()[i])
#     mails.append(x.body)


tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = TFDistilBertForSequenceClassification.from_pretrained("model")
pipe = TextClassificationPipeline(model = model, tokenizer = tokenizer, return_all_scores = False)


app = Flask(__name__) 
 
@app.route('/', methods = ['GET', 'POST']) 
def home():  
    return render_template('home.html');  

@app.route('/mails', methods = ['GET', 'POST'])
def mails():
    # print('0')
    text = request.form["text"]
    result = pipe(text)
    # print(type(result))
    score = result[0]['label']
    return render_template('mails.html', message = score)

@app.route('/inbox', methods = ['GET', 'POST'])
def inbox():
    ids = server.listids()
    # mails = []
    data_to_append = []
    header = ['Type','Date','Title','From','Body']
    file = open('mails.csv', 'a', newline = '')
    file.truncate(0)

    writer = csv.writer(file)

    for i in range(len(ids)):
        x = server.mail(server.listids()[i])
        mail = []
        result = pipe(x.body[:20])
        score = result[0]['label']
        if score == 'LABEL_0':
            mail.append('Safe')
        else:
            mail.append('Unsafe')
        # mail.append(score)
        mail.append(x.date)
        mail.append(x.title)
        mail.append(x.from_addr)
        mail.append(x.body)
        data_to_append.append(mail)

    # data_to_append.append(mails)
    writer.writerow(header)
    writer.writerows(data_to_append)
    file.close()
    file = open('mails.csv', 'r+', newline = '')
    df = csv.reader(file)
    # file.close()
    # file.truncate(0)
    print(0)
    return render_template("inbox.html", csv = df)

if __name__ == '__main__':  
    app.run(debug = True)
