from flask import Flask
from flask import render_template, redirect, request
from transformers import BertConfig, BertModel, TFDistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast
from transformers import TextClassificationPipeline
from transformers import DistilBertTokenizerFast
import csv
import easyimap as e


user = "*"   # Enter Gmail Address
password = "#"  # Password (Use App Password as google doesn't allow IMTP servers to access accounts directly since May - 2022)

server = e.connect("imap.gmail.com", user, password)
mails = []

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
model = TFDistilBertForSequenceClassification.from_pretrained("model")
pipe = TextClassificationPipeline(model = model, tokenizer = tokenizer, return_all_scores = False)


app = Flask(__name__) 
 
@app.route('/', methods = ['GET', 'POST']) 
def home():  
    return render_template('home.html');  

@app.route('/mails', methods = ['GET', 'POST'])
def mails():
    text = request.form["text"]
    result = pipe(text)
    score = result[0]['label']
    return render_template('mails.html', message = score)

@app.route('/inbox', methods = ['GET', 'POST'])
def inbox():
    ids = server.listids()
    data_to_append = []
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
        mail.append(x.date)
        mail.append(x.title)
        mail.append(x.from_addr)
        mail.append(x.body)
        data_to_append.append(mail)

    writer.writerows(data_to_append)
    file.close()
    file = open('mails.csv', 'r+', newline = '')
    df = csv.reader(file)
    print(0)
    return render_template("inbox.html", csv = df)

if __name__ == '__main__':  
    app.run(debug = True)
