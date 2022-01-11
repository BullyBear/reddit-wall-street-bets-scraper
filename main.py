from flask import Flask, request, redirect, url_for, render_template, Blueprint, jsonify, make_response
# from flask_restful import Resource, Api
from flask_restplus import Api, Resource, fields, apidoc
# import flask_restx
# from flask_restx import Resource, Api, fields
from flask_cors import CORS, cross_origin
import requests
import traceback
import numpy as np
import pandas as pd
import json



server = Flask(__name__)
CORS(server)

app = Api(server)

blueprint = Blueprint('wsb', 'wsb')

# app = flask_restx.Api(app = blueprint, 
app = Api(app = blueprint, 
      version = "1.0", 
      title = "r/WallStreetBets", 
      description = "Find most discussed stocks today on r/WallStreetBets"
      )


server.register_blueprint(blueprint, url_prefix='/wall-street-bets')



@app.route('/top-stocks')
class WallStreetBets(Resource):
# class WallStreetBets(flask_restx.Resource):


    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

            
    def get(self):
    # def post(self):
        category = request.args["selectedCategory"]
        print(category)
        try:

            url = "https://wallstreetbets.p.rapidapi.com/"
            querystring = {"date":"today"}
            querystringTwo = {"date":"this_week"}
            querystringThree = {"date":"this_month"}
            headers = {
                'x-rapidapi-host': "wallstreetbets.p.rapidapi.com",
                'x-rapidapi-key': "4a84fad910msha335a71778de51cp1a79d6jsnafac3cffa115"
            }

             # response = requests.request("GET", url, headers=headers, params=querystring)
            if category=="today":
                response = requests.request("GET", url, headers=headers, params=querystring)
                form_data = response.text
                print(form_data)
            if category=="this_week":
                response = requests.request("GET", url, headers=headers, params=querystringTwo)
                form_data = response.text
            if category=="this_month":
                response = requests.request("GET", url, headers=headers, params=querystringThree)
                form_data = response.text
            # return jsonify(form_data)
            return json.loads(form_data)
        except Exception as error:
            traceback.print_exc()
            return jsonify({
                "statusCode": 500,
                "status": "Could not find stocks",
                "error": str(error)
            })






if __name__ == '__main__':
    server.run(debug=True)







    