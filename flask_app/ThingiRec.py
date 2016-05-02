from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import psycopg2
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time

app = Flask(__name__)
full_df = None
vec_X = None

def get_top_users_and_parts(user_ind, username):
    # df_user_removed = df.drop(user_ind, axis = 0, inplace = False)
    # X_user_removed = np.delete(X, user_ind, axis = 0)
    n_items = 5

    base_ids = full_df.iloc[user_ind]['item_id']
        
    # limit number of parts to be used for similarity analysis
    num_user_parts = min(20,len(user_ind))
    user_ind=np.random.choice(user_ind,(num_user_parts,))

    while True:
        similar_users = []
        similar_parts = []
        
        for i in user_ind:
            # base_item = vec_X[i].reshape(1, -1)
            base_item_id = full_df.iloc[i]['item_id']
            # distances_vector = np.apply_along_axis(lambda x: cosine(x,base_item), 1, vec_X)
            # distances_vector = linear_kernel(base_item, vec_X)
            distances_vector = linear_kernel(vec_X[i:i+1], vec_X).flatten()
            similar_indices = np.argsort(distances_vector)[::-1]
            similar_items = full_df.iloc[np.ravel(similar_indices[:n_items])]

            similar_users.extend(list(similar_items['username']))
            similar_parts.extend(list(similar_items['item_id']))

        similar_users_set = set(similar_users)
        similar_parts_set = set(similar_parts)

        similar_users_set.discard(username)
        for item_id in base_ids:
            similar_parts_set.discard(item_id)

        if len(similar_users_set) >= 5:
            break
        else:
            n_items += 2

    top_similar_users = sorted(similar_users_set, key = lambda x: similar_users.count(x), reverse = True)[:5]

    top_similar_parts = sorted(similar_parts_set, key = lambda x: similar_parts.count(x), reverse = True)[:5]
    similar_parts_df = full_df[full_df['item_id'].isin(top_similar_parts)].set_index('item_id')
    part_names = similar_parts_df['item_name']
    part_ids = part_names.keys()

    # limit length of part names
    max_len = 15

    part_names = map(lambda x: x[:max_len+1]+'...' if len(x) > max_len else x,part_names)

    return top_similar_users, part_ids, part_names

@app.route('/')
def api_root():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    rec_start = time.time()
    print "recommending!!!"
    username = str(request.form['user_input']).lower()
    user_ind = np.ravel(np.argwhere(full_df['username']==username))

    # if the username is found, get recommendations
    # otherwise, reroute user to try again
    if user_ind.any():
        users, part_numbers, part_names = get_top_users_and_parts(user_ind, username)
        rec_end = time.time()
        print "time to recommend: {}".format(rec_end-rec_start)
        return render_template('recommend.html', users=users, part_numbers=part_numbers, part_names=part_names)
    else:
        print "empty dataframe"
        return render_template('try_again.html', username=username)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    boot_start = time.time()
    # connect to database
    conn = psycopg2.connect(dbname='thingiscrape', user='ec2-user', host='/tmp')
    c = conn.cursor()

    # query database
    SQL = "SELECT * FROM thingi_items ORDER BY item_id"
    c.execute(SQL)
    full_df = pd.DataFrame(c.fetchall(), columns = ['item_id','item_name','description','username'])
    full_df['username']=full_df['username'].apply(lambda x: x.lower())
    full_df['item_name']=full_df['item_name'].apply(lambda x: x.lower())
    full_df['description']=full_df['description'].apply(lambda x: x.lower())

    # transform names and descriptions
    tfidfvect = TfidfVectorizer(stop_words='english', max_features = 1000)
    documents_vec = full_df['item_name'] + ' ' + full_df['description']
    vec_X = tfidfvect.fit_transform(documents_vec)
    del documents_vec

    boot_end = time.time()
    print "Ready :)"
    print "boot time: {}".format(boot_end-boot_start)

    # Start Flask app
    app.run(host='0.0.0.0', port=8000, debug=False)
