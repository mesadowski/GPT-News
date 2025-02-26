# GPT-News
This is a Flask application that's a kind of mashup between a news reader and ChatGPT. I started with a Flask tutorial from Digital Ocean (https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3) and modified it so that instead of storing and displaying blog posts, we grab a news feed from CNN, ask ChatGPT to read it using the ChatGPT API, and then ask ChatGPT to segue to a (hopefully funny) sales pitch for a product. The CSS and HTML files are very similar to those in the tutorial app. 

You need to get an OpenAI API token and insert it into the code where indicated. 

Note that there's a race condition here which I didn't bother fixing. I wait 1 day between refreshes of the content limit the charges from OpenAI's API. However if a number of users hit the site just as we reach 1 day from the last refresh, each one of them could trigger refreshes of the content and the charges might be higher than expected. 
