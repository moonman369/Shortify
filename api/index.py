from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint, Flask
import json
import os
from werkzeug.utils import secure_filename
# from mongopy import MongoOp





from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoOp:

    def __init__(self):
        self.uri = "mongodb+srv://moonman369:ayan%23123@cluster0.gblpsp7.mongodb.net/?retryWrites=true&w=majority"
        self.db = None
        self.collection = None
    
    def connect(self, db_name):
        client = MongoClient(self.uri)
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.db = client.get_database(db_name)
            return self.db
        except Exception as e:
            print(e)

    def get_collection(self, collection_name):
        try:
            self.collection = self.db[collection_name]
            print(f"Found collection: {collection_name}")
            return self.collection
        except Exception as e:
            print(e)

    def insert(self, insert_dict):
        try:
            self.collection.insert_one(insert_dict)
            print("Insert successful -->",insert_dict)
        except Exception as e:
            print(e)

    def find(self, short):
        try:
            res = self.collection.find_one(short)
            print(f"Result for \"{short}\":", res)
            return res["url"] if res else None
        except Exception as e:
            print(e)

    def delete_all(self):
        try:
            self.collection.delete_many({})
            print("Deleted all documents from collection.")
        except Exception as e:
            print(e)



# mongo = MongoOp()
# mongo.connect("shortify")
# mongo.get_collection("urlList")

# # mongo.insert({"short":"lsn", "url":"https://lensin-beta.netlify.com"})
# mongo.delete_all()
# print(mongo.find({"short":"hi"}))





mongo = MongoOp()
mongo.connect("shortify")
mongo.get_collection("urlList")

app = Flask(__name__)
app.secret_key = '  yomommasofatshebendslight'

uri = "mongodb+srv://moonman369:ayan%23123@cluster0.gblpsp7.mongodb.net/?retryWrites=true&w=majority"



@app.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('url_list.json'):
            with open('url_list.json') as urls_file:
                # print(urls_file)
                urls = json.load(urls_file)

        # if request.form['code'] in urls.keys():
        if mongo.find({"short":request.form['code']}):
            flash('Short name is already in use. Please try another one.')
            return redirect(url_for('home'))
        
        if 'url' in request.form.keys():
        #    urls[request.form['code']] = {'url': request.form['url']}
            mongo.insert({"short":request.form['code'], "url":request.form['url']})
        else: 
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            # print(os.cwd())
            if not os.path.exists('api/static/user_files'):
                os.chdir('api/static')
                os.mkdir('user_files')
            f.save(os.path.join(f'{os.getcwd()}/user_files', full_name))
            urls[request.form['code']] = {'file': full_name}

        # with open('url_list.json', 'w') as url_file:
        #     json.dump(urls, url_file)
        session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else: 
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    # if mongo.find(code):
    #     return redirect()
    # if os.path.exists('url_list.json'):
    #     with open('url_list.json') as urls_file:
    #         urls = json.load(urls_file)
    #         if code in urls.keys():
    #             if 'url' in urls[code].keys():
    #                 return redirect(urls[code]['url'])
    #             else:
    #                 print(os.getcwd())
    #                 return redirect(url_for('api/static', filename=f'user_files/' + urls[code]['file']))
    return redirect(mongo.find({"short":code})) if mongo.find({"short":code}) else abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == "__main__":
    app.run(port=8001)