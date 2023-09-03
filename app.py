from flask import Flask,render_template,request,redirect,url_for
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similar.pkl','rb'))

contact_info = {
    'name': 'Aviroop Mitra',
    'email': 'aviroopmitra5@gmail.com',
    'contact': '+91 79809 58951',
    'linkedin': 'https://www.linkedin.com/in/aviroop-mitra-a98150225/'
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['No. of ratings'].values),
                           rating=list(round(n,2) for n in popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input in pt.index: 
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[0:7]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        print(data)
        return render_template('recommend.html',data=data)
    else :
        return render_template('recommend.html',nope="NA")

@app.route('/contact')
def contact_ui():
    return render_template('contact.html',contact = contact_info)
    

if __name__ == '__main__':
    app.run(debug=True)