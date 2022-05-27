import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import bs4 as bs
import urllib.request
import pickle


# load the nlp model and tfidf vectorizer from disk
filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl','rb'))

def get_title_index(df,index):
    return df[df.index == index]["movie_title"].values[0]
def get_index_from_title(df,title):
    return df[df.movie_title==title]["index"].values[0]

def create_similarity():
    df=pd.read_csv("data.csv")
    cv=CountVectorizer()
    count_matrix=cv.fit_transform(df["comb"])
    cosine_sim=cosine_similarity(count_matrix)
    return df,cosine_sim


  

def recommendations(m):
    m = m.lower()
    df,cosine_sim=create_similarity()
    if m not in df['movie_title'].unique():
        return('Oops!! This movie is not avaliable')
    else:
        l=[]
        i=0
        movie_index=get_index_from_title(df,m)
        similar_movies=list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies=sorted(similar_movies,key=lambda x:x[1],reverse=True)
        for movie in sorted_similar_movies:
            l.append(get_title_index(df,movie[0]))
            i=i+1
            if i>20:
                break
        return l    

    
# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list



app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/similarity",methods=["POST"])
def similarity():
    movie = request.form['name']
    rc = recommendations(movie)
    if type(rc)==type('string'):
        return rc
    else:
        m_str="---".join(rc)
        return m_str

@app.route("/recommend",methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_posters = request.form['rec_posters']



    # call the convert_to_list function for every string that needs to be converted to list
    rec_movies = convert_to_list(rec_movies)
    rec_posters = convert_to_list(rec_posters)


    movie_cards = {rec_posters[i]: rec_movies[i] for i in range(len(rec_posters))}
    # web scraping to get user reviews from IMDB site
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})
    
    reviews_list = [] # list of reviews
    reviews_status = [] # list of comments (good or bad)
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
            # passing the review to our model
            movie_review_list = np.array([reviews.string])
            movie_vector = vectorizer.transform(movie_review_list)
            pred = clf.predict(movie_vector)
            reviews_status.append('Good' if pred else 'Bad')

    # combining reviews and comments into a dictionary
    movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     

    # passing all the data to the html file
    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
        vote_count=vote_count,release_date=release_date,runtime=runtime,status=status,genres=genres,
        movie_cards=movie_cards,reviews=movie_reviews)

if __name__ == "__main__":
    import warnings
    warnings.warn("use 'python -m nltk', not 'python -m nltk.downloader'",         DeprecationWarning)
    app.run_server(debug=True)
