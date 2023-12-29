from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

# BASE RESULTADOS
# Fonte: https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx
df = pd.read_excel('Mega-Sena.xlsx').fillna('')
df = df.filter(items=['Concurso', 'Data do Sorteio', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6'])
df = df.to_dict('records')

for i in df:
    i["num_sorteados"] = (i["Bola1"],i["Bola2"],i["Bola3"],i["Bola4"],i["Bola5"],i["Bola6"])

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({"response":"Bem vindo!","status":200})

@app.route("/resultados")
def resultados():
    return jsonify(df)

@app.route("/palpite", methods=["POST"])
def palpite():
    palpite_num = request.get_json()
    resultados_mega = df

    for item in resultados_mega:
        num_acertos = 0
        for n in palpite_num:
            if n in item["num_sorteados"]:
                num_acertos += 1

            item["qnt_acerto"] = num_acertos

    resultados_mega = [ i for i in resultados_mega if i["qnt_acerto"] != 0 ]

    return jsonify(resultados_mega)

if __name__=='__main__':
    app.run(debug=True)
