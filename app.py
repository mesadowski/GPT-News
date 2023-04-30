
from flask import Flask, render_template
import random
from datetime import datetime,timedelta

import feedparser
import openai   

def get_main_text(j, p,link):
    
    prompt_text = "Read and briefly summarize the news story at this link: {}. \
        and use it to explain why one should want to buy a product: the {}. Make it funny and brief.".format(link, p)

    print(prompt_text)
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_text,
      temperature=0.6,
      max_tokens=200
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

def create_posts():
    
    NewsFeed = feedparser.parse('https://www.etonline.com/news/rss')
    num_entries = len(NewsFeed.entries)
    print('number of news stories = ',num_entries)
    posts = []
    for i in range(0,NUM_POSTS):
        prod = products [random.randint(0,len(products)-1)]
        entry = NewsFeed.entries[i]
        link = entry['link']
        print(entry['link'])
        text = get_main_text(i,prod,link)
        title = get_title(prod,text)
        summary = text[:300]+'.....'
        posts.append([i,prod,title,text,summary,link])
        last_run = datetime.now()
        print('last run = ',last_run)
    return posts, last_run

products = ['Ronco Veg-o-Matic', 'K-tel Fishin Magician', 'Snuggie Blanket', 'Ronco Mr. Microphone','Navage Nasal Irrigation System']

NUM_POSTS = 5

random.seed(9876)

openai.api_key = '<YOURKEYGOESHERE>'

all_posts, last_run = create_posts()

app = Flask(__name__)

@app.route('/')
def index():
    global last_run
    global all_posts
    time_passed = datetime.now() - last_run
    print ('last run = ',last_run, 'time passed =', time_passed.days)
    if time_passed.days >= 1:
        print('rerun it')
        all_posts, last_run = create_posts()
    return render_template('index.html', posts=all_posts)

@app.route('/<int:post_id>')
def post(post_id):
    global all_posts
    return render_template('post.html', post=all_posts[post_id])

@app.route('/#')
def about():
    return render_template('about.html')

