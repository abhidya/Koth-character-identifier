import json
import os

from flask import Flask, render_template, request

try:
    from flask_compress import Compress
except ImportError:
    Compress = None


class OfflineKothModel:
    """Small deterministic classifier used when legacy ML dependencies are absent."""

    keywords = {
        "hank": {"propane", "work", "tool", "lawn", "neighbor"},
        "bobby": {"joke", "funny", "dance", "school", "snack"},
        "peggy": {"spanish", "teacher", "genius", "essay", "class"},
        "dale": {"conspiracy", "pocket", "rusty", "government", "alien"},
    }

    def predict_sims(self, text):
        words = {word.strip(".,!?;:").lower() for word in text.split()}
        scored = []
        for label, terms in self.keywords.items():
            score = 0.5 + (0.1 * len(words & terms))
            scored.append((label, round(score, 3)))
        return sorted(scored, key=lambda item: item[1], reverse=True)


OFFLINE_TWEETS = [
    "I tell you what, propane and lawn work make a fine afternoon.",
    "That school dance joke was funny enough for extra snacks.",
    "My Spanish class essay proves I am a genius teacher.",
    "The government alien conspiracy fits in my pocket.",
]

app = Flask(__name__)
compress = Compress() if Compress else None
model = None
model_error = None


def get_model():
    global model, model_error
    if model is not None:
        return model

    if os.environ.get("KOTH_LIVE_MODEL") != "1":
        model = OfflineKothModel()
        return model

    try:
        from ml import build_model

        model = build_model()
    except Exception as exc:
        model_error = str(exc)
        model = OfflineKothModel()
    return model


def get_tweets(handle):
    if handle.lower() in {"demo", "offline", "fixture"}:
        return OFFLINE_TWEETS

    try:
        from twitter import hitting_twitter

        return hitting_twitter(handle)
    except Exception as exc:
        return "Twitter Search Error: {}. Try handle 'demo' for offline mode.".format(exc)


@app.route('/')
def hello_world():
    return render_template('mini_index.html')


@app.route('/health')
def health():
    return {
        "ok": True,
        "mode": "live" if os.environ.get("KOTH_LIVE_MODEL") == "1" else "offline",
        "model_error": model_error,
    }


@app.route('/results', methods=['GET', 'POST'])
def results():
    input_values = request.form.getlist('twittername')
    handle = input_values[0] if input_values else "demo"
    tweets = get_tweets(handle)
    if isinstance(tweets, str) and tweets.startswith("Twitter Search Error"):
        return json.dumps({"ERROR": tweets}, indent=4, sort_keys=True, default=str), 200

    predictor = get_model()
    json_tweets = [{tweet: predictor.predict_sims(tweet)} for tweet in tweets]
    return json.dumps(json_tweets, indent=4, sort_keys=True, default=str), 200


if __name__ == "__main__":
    if compress:
        compress.init_app(app)
    try:
        from waitress import serve

        serve(app, host='0.0.0.0', port=8000)
    except ImportError:
        app.run(host='0.0.0.0', port=8000)
