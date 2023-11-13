from flask import session
from anime_flask import app
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import SnowballStemmer
import re
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec 
from gensim.models.doc2vec import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score
from anime_flask.routing.basic.constructors import *
import json

# Function for cleaning sentence
def clean_synopsis(text):
    # Remove stop words
    stops = set(stopwords.words("english"))
    words = [w for w in text.lower().split() if not w in stops]
    final_text = " ".join(words)
    # Special Characters
    review_text = re.sub(r"[^A-Za-z0-9(),!.?\'\`]", " ", final_text )
    review_text = re.sub(r"\'s", " 's ", final_text )
    review_text = re.sub(r"\'ve", " 've ", final_text )
    review_text = re.sub(r"n\'t", " 't ", final_text )
    review_text = re.sub(r"\'re", " 're ", final_text )
    review_text = re.sub(r"\'d", " 'd ", final_text )
    review_text = re.sub(r"\'ll", " 'll ", final_text )
    review_text = re.sub(r",", " ", final_text )
    review_text = re.sub(r"\.", " ", final_text )
    review_text = re.sub(r"!", " ", final_text )
    review_text = re.sub(r"\(", " ( ", final_text )
    review_text = re.sub(r"\)", " ) ", final_text )
    review_text = re.sub(r"\?", " ", final_text )
    review_text = re.sub(r"\s{2,}", " ", final_text )
    return review_text

@app.before_first_request
def doc2vec_recomendation():
    df_clean = pd.read_sql_table("doc_vec", dataURI)
    # Put dataframe into a global variable
    session["df_clean"]=df_clean
    
#     # Label Synopsis
#     new_synopsis = df_clean['model'].tolist()
#     labeled_synopsis=[]
#     for i in range(len(df_clean)):
#         try:
#             labeled_synopsis.append(TaggedDocument(new_synopsis[i].split(), df_clean[df_clean.index == i].anime_id))
#         except:
#             continue
        
#     # Build Model Doc2Vec
#     model=Doc2Vec()
#     model = Doc2Vec(dm = 1, min_count=1, window=10, size=150, sample=1e-4, negative=10)
#     model.build_vocab(labeled_synopsis)
    
#     # Train the model with 20 epochs
#     for epoch in range(4):
#         model.train(labeled_synopsis,epochs=model.iter,total_examples=model.corpus_count)
#         print("Epoch #{} is complete.".format(epoch+1))
    
#     # Put model into a global model
#     session["doc_model"] = model
#     print(session.keys())
    
# @app.route('/des_res')
# def des_res():
#     df_sentence = pd.read_sql_table("user_sentence", dataURI)
#     sentence = df_sentence.iloc[0].sentence
#     scores = []
#     print(session["df_clean"].head())
#     for i in range(len(session["df_clean"])):
#         try:
#             scores.append(session["doc_model"].wv.n_similarity(clean_synopsis(sentence).split(), session["df_clean"].iloc[i]['model'].split()))
#         except:
#             scores.append(0)
#     df_chosen = session["df_clean"]
#     df_chosen["similarity"] = scores
#     df_chosen = df_chosen.sort_values(by=['similarity'], ascending=False)
#     df_chosen = df_chosen.reset_index(drop=True)
#     df_chosen = df_chosen.head()
#     result = df_chosen.to_json(orient="records")
#     parsed = json.loads(result)
#     return jsonify(parsed)