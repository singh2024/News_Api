from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
from translate import Translator
import time

app = Flask(__name__)
api = Api(app)
CORS(app)

url = "https://bing-news-search1.p.rapidapi.com/news"
translator = Translator("fr")

querystring = {"safeSearch": "Off", "textFormat": "Raw"}

headers = {
    "X-BingApis-SDK": "true",
    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com",
    "X-RapidAPI-Key": "fb3b49dc13msh62af094bdc358fep181dc7jsn4271647c6186"
}


class News(Resource):
    def get(self):
        try:
            global url
            response = requests.request("GET", url, headers=headers, params=querystring)

            news = response.json()["value"]
            data = {"news": []}

            for item in news:
                title = item["name"]
                desc = item["description"]
                title_french = translator.translate(title)
                desc_french = translator.translate(desc)
                url = item["url"]
                timestamp = time.time()

                news_data = {
                    "title_en": title,
                    "desc_en": desc,
                    "title_fr": title_french,
                    "desc_fr": desc_french,
                    "timestamp": round(timestamp),
                    "image_url": url
                }

                data["news"].append(news_data)

            return data

        except:
            return {'data': 'An Error Occurred during fetching Api'}


api.add_resource(News, '/')

if __name__ == '__main__':
    app.run()
