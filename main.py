from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from joblib import load
import pandas as pd


app = Flask(__name__)
api = Api(app)
modelo = load('ML.joblib')

class Pricing(Resource):
    @app.route("/")
    def hello_world():
        return "<p>Hellom world<p>"
    def post(self):
        args = request.get_json(force=True)

        # Certifique-se de que a entrada é um dicionário Python
        if not isinstance(args, dict):
            return jsonify({'error': 'Entrada inválida'})

        # Converta o dicionário em um DataFrame pandas
        input_df = pd.DataFrame(args, index=[0])

        # Verifique se o DataFrame tem as colunas corretas
        expected_columns = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty',
                            'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm',
                            'product_category_name']
        if not set(input_df.columns) == set(expected_columns):
            return jsonify({'error': 'Colunas incorretas no DataFrame'})
        
        predict = modelo.predict(input_df)[0]

        return jsonify({'previsão': float(predict)})

api.add_resource(Pricing, '/')

if __name__ == '__main__':
    app.run()
