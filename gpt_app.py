
from flask import Flask, render_template
#from werkzeug.exceptions import abort
#from datetime import datetime
import random

import feedparser
import openai   

NUM_POSTS = 3 

openai.api_key ='<key goes here>'

NewsFeed = feedparser.parse('http://rss.cnn.com/rss/cnn_topstories.rss')
num_entries = len(NewsFeed.entries)

products = ['Ronco Veg-o-Matic', 'K-tel Fishin Magician', 'Ginsu Knife', 'Snuggie Blanket', 'Ronco Mr. Microphone']

app = Flask(__name__)

def get_main_text(j, p):
    
    entry = NewsFeed.entries[j]
    link = entry['link']
    #summary = entry['summary']
    
    print(entry['link'])
    
    prompt_text = "Read and briefly summarize the news story at this link: {}. \
        and use it to explain why one should want to buy a product: the {}. Make it funny and brief.".format(link, p)

    print(prompt_text)
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_text,
      temperature=0.6,
      max_tokens=150
    )

    return response.choices[0].text

def get_title(p,prior_convo):
    # Note: you need to feed back the prior output so that the API has this as context
    prompt_text = "Using this: {} write a brief, funny headline in only 10 words or less.".format(prior_convo)
    print(prompt_text)
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_text,
      temperature=0.1,
      max_tokens=50
    )

    return response.choices[0].text

all_posts = []
for i in range(0,NUM_POSTS):
    prod = products [random.randint(0,len(products)-1)]
    text = get_main_text(i,prod)
    title = get_title(prod,text)
    all_posts.append([i,prod,title,text])

@app.route('/')
def index():
    return render_template('index.html', posts=all_posts)

@app.route('/<int:post_id>')
def post(post_id):
    return render_template('post.html', post=all_posts[post_id])

