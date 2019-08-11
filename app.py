from flask import Flask, render_template, request
from twitter import hitting_twitter
from ml import build_model
import json
from flask_compress import Compress

from waitress import serve

app = Flask(__name__)
# app.debug = True
# app.secret_key = 'development key'
x = build_model()
compress = Compress()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    input_values = request.form.getlist('twittername')
    print(input_values)
    tweets = hitting_twitter(input_values[0])
    if tweets == "Twitter Search Error: Is the username correct":
        return json.dumps({"ERROR": tweets}, indent=4, sort_keys=True, default=str), 200
    # json_tweets = [{'getting a good night s sleep boring too dark i just go unconscious drinking 27 cups of coffee lit af terrifies my roommate craig i can see god': [('peggy', 0.9639838337898254), ('hank', 33.9637914299964905), ('dale', 0.9618546366691589), ('bobby', 0.9613964557647705)]}, {'and they wonder why we marginalized students need our own spaces on campus check the stats …': [('peggy', 0.9626613259315491), ('hank', 0.9620893597602844), ('dale', 0.9607207775115967), ('bobby', 0.9598737955093384)]}, {'As a licensed psychologist I want to say three things 1 White supremacy is not a mental disorder 2 Mental illness is not synonymous with homicidal tendencies 3 Video games do not cause mental illness or homicidal behavior': [('peggy', 0.9830300807952881), ('dale', 0.9818015098571777), ('hank', 0.9814910888671875), ('bobby', 0.981253445148468)]}, {'When your crush hits ya with that linkedin connection request': [('bobby', 0.9322543144226074), ('hank', 0.9301737546920776), ('peggy', 0.9301366806030273), ('dale', 0.9290658831596375)]}, {'2019 mass shootings 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 3 249 repost': [('hank', 0.06592932343482971), ('dale', 0.06421639025211334), ('bobby', 0.0627744123339653), ('peggy', 0.057141438126564026)]}, {'Loved the flood warning I got after I drove my motorcycle home in the rain': [('bobby', 0.8203638792037964), ('hank', 0.8171078562736511), ('peggy', 0.8154168128967285), ('dale', 0.8118678331375122)]}, {'In higher ed we talk a lot about diversity and diversity programming but very little of that discussion focuses on socioeconomic status because it s not always immediately visible and discussions about money make people uncomfortable': [('bobby', 0.9798437356948853), ('hank', 0.9790008664131165), ('dale', 0.9782710075378418), ('peggy', 0.9779518842697144)]}, {'I would just like to formally announce that I m back on my bullshit': [('bobby', 0.7830278277397156), ('peggy', 0.7826418876647949), ('dale', 0.7817957401275635), ('hank', 0.7817666530609131)]}, {'If you think you re a leader and you turn around and no one is following you then you re simply out for a walk': [('peggy', 0.9850124716758728), ('hank', 0.9833850860595703), ('dale', 0.9825080633163452), ('bobby', 0.9822404384613037)]}, {'I just logged into my student loan account for the first time since Freshman Year and now I m sad Who is finna join me for my debt free celebration in December 2031': [('dale', 0.9613476991653442), ('hank', 0.9591951370239258), ('peggy', 0.9582904577255249), ('bobby', 0.9579288363456726)]}, {'I posted a sappy snap about moving away from my roommates and they are hitting me with all these emotions and I can t handle it': [('dale', 0.9381486773490906), ('peggy', 0.9380826354026794), ('hank', 0.937880277633667), ('bobby', 0.9347798824310303)]}, {'Y all I really just went through one of the best weeks of my life I m energized for this year I m working on me My eSports team just won in a huge upset I m getting ready to move to a new place': [('peggy', 0.9921051859855652), ('hank', 0.9917133450508118), ('dale', 0.9916977882385254), ('bobby', 0.9915771484375)]}, {'feelsgoodman GG pic twitter com JVoQDyWDff': [('peggy', -0.32198673486709595), ('hank', -0.32253122329711914), ('dale', -0.32723477482795715), ('bobby', -0.32741957902908325)]}, {'Just because you are it doesn t mean you understand': [('bobby', 0.889556884765625), ('peggy', 0.8884443044662476), ('dale', 0.8875531554222107), ('hank', 0.8861321210861206)]}, {'The security staff and bouncers at are racist and unprofessional Please read pic twitter com qjFpTI0oSj': [('peggy', 0.8316916227340698), ('hank', 0.8286184072494507), ('bobby', 0.8251796364784241), ('dale', 0.8234989643096924)]}, {'DID YALL KNOW THE SUB MR SCOTT PASSED i just found out': [('dale', 0.9057146906852722), ('hank', 0.9024478793144226), ('bobby', 0.901611328125), ('peggy', 0.9012407064437866)]}, {'My dad posted this photo of lil bad ass mepic twitter com Vpmj7QH6oB': [('bobby', 0.8352470397949219), ('dale', 0.8341977000236511), ('hank', 0.8332484364509583), ('peggy', 0.8329951763153076)]}, {'I had coffee at like 10 pm and now I m trapped': [('peggy', 0.9697150588035583), ('dale', 0.9675013422966003), ('hank', 0.9674116373062134), ('bobby', 0.9662372469902039)]}, {'Me ehhhhh I m not going to watch this season of Queer eye 2 hours later Me sobbing Karamo you really just went there': [('peggy', 0.949542224407196), ('bobby', 0.9491580724716187), ('hank', 0.9489762187004089), ('dale', 0.9478299617767334)]}, {'KKK has killed 5000 Americans since 1865 •Not designated as terror org White Nationalists have killed 313 Americans since 1995 •Not designated as terror org Antifa has killed 0 Americans—ever •This is clearly a terror org …': [('peggy', 0.980783998966217), ('hank', 0.9805598855018616), ('dale', 0.9802777171134949), ('bobby', 0.9796247482299805)]}]
    json_tweets = []
    for tweet in tweets:
        tweet = {tweet: x.predict_sims(tweet)}
        json_tweets.append(tweet)
    json_tweets = json.dumps(json_tweets, indent=4, sort_keys=True, default=str)
    return json_tweets, 200


if __name__ == "__main__":
    # app.run() ##Replaced with below code to run it using waitress
    compress.init_app(app)
    serve(app, host='0.0.0.0', port=8000)
