
My website that reads your tweets and uses AI to figure out who you are from King of the Hill!

Try it out here http://kingofthehill.duckdns.org:8001/

I use Doc2Vec with Data (Tweets) scrapped from a twitter user to find who you are most like from King of the Hill

Currently only classifying Hank, Bobby, Peggy and Dale

## Local setup

Create a local virtual environment instead of committing one to the repo:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app depends on older Twitter scraping behavior and older Python package versions, so treat this as a legacy research/demo project until the scraping layer and dependencies are refreshed.

TO DO:

Model:
  Try new models (RF, Bert)
  Better Tweet Preprocessing:
     Removing tweets like " Twitter Pic XXXX" , " ", one words
     
Documentation:
  Expanding Documentation and ReadMe
  
Python:
  Catch differences in user input
  Dont pull Retweets
  Multithread
  Restart Crash proof, Manage websites uptime
  Offline and crash notifications
  Logging
  
 JS:
  Better Visuals
  better classification (1,1,1,1) or (.99 , .99, .99, .99) are disregarded
  
 Html:
  More intuitive design ( scrolling is not intuitive)
  
  
