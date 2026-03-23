from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import psutil
import os
import time
import json

app = Flask(__name__, static_folder='static')

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/calcul')
def calcul():
    return render_template('calcul.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        
        # Paramètres
        G_prime = float(data.get('G_prime', 50))
        m = float(data.get('m', 25))
        L = float(data.get('L', 100))
        x0 = float(data.get('x0', 0.015))
        N_etages = int(data.get('N_etages', 3))
        
        # Chrono et RAM
        start_time = time.perf_counter()
        process = psutil.Process(os.getpid())
        mem_start = process.memory_info().rss
        
        # Calcul du facteur
        S = (G_prime * m) / L
        
        # Calcul vectorisé
        etages = np.arange(1, N_etages + 1)
        x_sortant = x0 / (1 + S) ** etages
        x_entrant = np.concatenate(([x0], x_sortant[:-1]))
        
        # Créer le dataframe
        df = pd.DataFrame({
            "Étage": etages.tolist(),
            "x_entrant": x_entrant.tolist(),
            "x_sortant": x_sortant.tolist()
        })
        
        # Chrono/RAM fin
        end_time = time.perf_counter()
        mem_end = process.memory_info().rss
        mem_used = (mem_end - mem_start) / (1024 ** 2)
        
        # Préparer la réponse
        response = {
            'S': round(S, 4),
            'table': df.to_dict(orient='records'),
            'etages': etages.tolist(),
            'x_entrant': [round(x, 6) for x in x_entrant.tolist()],
            'x_sortant': [round(x, 6) for x in x_sortant.tolist()],
            'execution_time': round(end_time - start_time, 6),
            'memory_used': round(mem_used, 6),
            'stats': {
                'x_entrant_min': round(float(x_entrant.min()), 6),
                'x_sortant_min': round(float(x_sortant.min()), 6),
                'mean_diff': round(float((x_entrant - x_sortant).mean()), 6)
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
