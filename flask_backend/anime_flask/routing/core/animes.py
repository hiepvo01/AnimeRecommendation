from anime_flask import app
from flask import session, url_for, redirect
from anime_flask.routing.basic.constructors import *
from sqlalchemy import desc
import requests
from bs4 import BeautifulSoup
from anime_flask.models.modelreps.model import *
import json
import pandas as pd
from wordcloud import STOPWORDS

def web(WebUrl):
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    link = s.find('iframe')['src']
    return link

def score_table(WebUrl):
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    link = s.find("table",{"class":"score-stats"})
    return link

def cloud_review(reviews):
    d = {}
    for review in reviews:
        sentence = review["text"]
        sentence = sentence[78:].lower()
        word_list = sentence.split(" ")
        stopwords = list(STOPWORDS)
        stopwords = stopwords + ["", "\n", "\n\n", "story", "animation", "sound", "character", "enjoyment", "\r\n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "episodes", "\r\nthe", "anime", "characters", "will", "episode", "episodes", "character", "it", "watch", "watching", "make", "makes", "\r\ni", "anime", "animes"]
        for word in word_list:
            if word not in stopwords:
                if word not in d:
                    d[word] = d.get(word,0) + 1
                else:
                    d[word] = d[word] + d.get(word,0) + 1
    sort = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    top_words = []
    i = 0
    for w in sort:
        if i == 35:
            break
        top_words.append({"word": w, "size" : (205 - i*6) * 0.5})
        i += 1
    return top_words

def global_data():
    return session["df_clean"], session["doc_model"]

@app.route("/animes/most_score", methods=['GET'])
def animes_score():
    animes_list = Angular.query.order_by(Angular.score.desc()).all()
    result = angulars_schema.dump(animes_list) 
    return jsonify(result)

@app.route("/animes/most_episode", methods=['GET'])
def animes_episode():
    animes_list = Angular.query.order_by(Angular.episodes.desc()).all()
    result = angulars_schema.dump(animes_list) 
    return jsonify(result)

@app.route("/animes/most_recent", methods=['GET'])
def animes_recent():
    animes_list = Angular.query.order_by(Angular.year.desc()).all()
    result = angulars_schema.dump(animes_list) 
    return jsonify(result)

@app.route("/animes/<anime_id>")
def anime_detail(anime_id):
    anime = Angular.query.filter_by(anime_id=anime_id).first()
    return angular_schema.dump(anime)

@app.route("/animes/<anime_id>/reviews")
def animes_review(anime_id):
    animes_list = Reviews.query.filter_by(anime_uid = anime_id).order_by(Reviews.order.desc()).all()
    result = reviews_schema.dump(animes_list) 
    return jsonify(result)

@app.route("/animes/<anime_id>/wordcloud")
def animes_wordcloud(anime_id):
    animes_list = Reviews.query.filter_by(anime_uid = anime_id).order_by(Reviews.order.desc()).all()
    result = reviews_schema.dump(animes_list)
    cloud_result = cloud_review(result)
    return jsonify(cloud_result)

@app.route("/animes/<anime_id>/episode/<episode_num>")
def anime_episodes(anime_id, episode_num):
    anime = Angular.query.filter_by(anime_id=anime_id).first()
    ep_url = angular_schema.dump(anime)['episode_url']

    result = {}
    result["ep_url"] = str(web(ep_url + "/" + str(episode_num)))
    r = json.dumps(result)
    loaded_r = json.loads(r)
    return loaded_r

@app.route("/animes/<anime_id>/stats")
def stats(anime_id):
    anime = Angular.query.filter_by(anime_id=anime_id).first()
    stat_url = angular_schema.dump(anime)['episode_url']
    stat_url = stat_url[:-7] + "stats"
    r = json.dumps({"score-table": str(score_table(stat_url))})
    loaded_r = json.loads(r)
    return loaded_r
    
@app.route("/animes/<anime_id>/similar_animes")
def anime_similar(anime_id):
  return jsonify(similar_animes(query=None,id=int(anime_id)))

@app.route("/search", methods=['POST'])
def search_anime():
    partial_name = request.json['partial_name']
    animes = Angular.query.filter(Angular.title.in_(part_id(partial_name))).all()
    result = angulars_schema.dump(animes)
    return jsonify(result)
    
@app.route('/description_rec', methods=['POST'])
def cosine_similar():
    UserSentence.query.delete()
    sentence = request.form['description']
    new_sentence = UserSentence(sentence = sentence)
    db.session.add(new_sentence)
    db.session.commit()
    print(sentence)
    return jsonify(message="You added sentence " + sentence), 201