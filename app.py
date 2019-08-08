from flask import Flask, render_template, request
from twitter import hitting_twitter
from ml import build_model
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'
x = build_model()


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    input_values = request.form.getlist('twittername')
    print(input_values)
    tweets = hitting_twitter(input_values[0])
    if tweets == "Twitter Search Error: Is the username correct":
        return json.dumps({"ERROR":tweets}, indent=4, sort_keys=True, default=str), 200
    json_tweets = []
    for tweet in tweets:
        tweet = {tweet: x.predict_sims(tweet)}
        json_tweets.append(tweet)
    json_tweets = json.dumps(json_tweets, indent=4, sort_keys=True, default=str)
    return json_tweets, 200


if __name__ == '__main__':
    app.run(debug=True)
