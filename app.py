"""
Application Flask - Plateforme de calcul de désorption
Structure:
- app.py (ce fichier)
- requirements.txt
- templates/ (HTML files)
  - accueil.html
  - calcul.html
- static/ (CSS, JS, images)
  - css/ (style.css, accueil.css, calcul.css)
  - js/ (script.js, calcul.js)
  - images/ (profile.jpg)
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import pandas as pd
import psutil
import os
import time
import base64
from pathlib import Path
from io import BytesIO

# Initialiser l'app Flask
app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')

# ========================
# INITIALISATION
# ========================

# Créer les dossiers nécessaires
Path('static/images').mkdir(parents=True, exist_ok=True)
Path('static/css').mkdir(parents=True, exist_ok=True)
Path('static/js').mkdir(parents=True, exist_ok=True)

@app.route('/')
def accueil():
    """Page d'accueil"""
    return render_template('accueil.html')


@app.route('/calcul')
def calcul():
    """Page de calcul"""
    return render_template('calcul.html')


@app.route('/get-profile-image')
def get_profile_image():
    """Endpoint pour servir l'image de profil"""
    try:
        image_path = Path('static/images/profile.jpg')
        
        if not image_path.exists():
            image_path = Path('static/images/profile.png')
        
        if image_path.exists():
            with open(image_path, 'rb') as f:
                image_data = f.read()
            # Retourner l'image directement
            return send_file(
                BytesIO(image_data),
                mimetype='image/jpeg' if image_path.suffix.lower() == '.jpg' else 'image/png',
                as_attachment=False
            )
        else:
            # Si l'image n'existe pas, retourner une placeholder
            return jsonify({'error': 'Image non trouvée', 'path': str(image_path)}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/setup')
def setup():
    """Page d'aide pour configurer l'app"""
    image_folder = Path('static/images')
    images = list(image_folder.glob('profile.*')) if image_folder.exists() else []
    
    image_status = "✅ Image trouvée" if images else "❌ Image non trouvée"
    
    return f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Configuration - Plateforme de Calcul</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }}
            h1 {{
                color: #667eea;
                margin-bottom: 30px;
            }}
            .section {{
                margin-bottom: 30px;
                border-left: 4px solid #667eea;
                padding-left: 20px;
            }}
            .status {{
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-weight: bold;
            }}
            .status.ok {{
                background: #d4edda;
                color: #155724;
            }}
            .status.error {{
                background: #f8d7da;
                color: #721c24;
            }}
            .btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                text-decoration: none;
                display: inline-block;
                margin-right: 10px;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }}
            code {{
                background: #f0f0f0;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚙️ Configuration de l'Application</h1>
            
            <div class="section">
                <h2>📸 Image de Profil</h2>
                <div class="status {'ok' if images else 'error'}">
                    {image_status}
                </div>
                <p>L'image de profil doit être placée dans : <code>static/images/profile.jpg</code></p>
                <br>
                <a href="/upload-profile" class="btn">📤 Uploader l'image</a>
            </div>
            
            <div class="section">
                <h2>✅ Structure du projet</h2>
                <p>Les dossiers suivants ont été créés automatiquement:</p>
                <ul>
                    <li>✓ <code>static/images/</code></li>
                    <li>✓ <code>static/css/</code></li>
                    <li>✓ <code>static/js/</code></li>
                    <li>✓ <code>templates/</code></li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🚀 Démarrage</h2>
                <p>L'application est prête ! Vous pouvez:</p>
                <a href="/" class="btn">Aller à l'accueil</a>
                <a href="/calcul" class="btn">Aller au calcul</a>
            </div>
        </div>
    </body>
    </html>
    '''
def upload_profile():
    """Page et endpoint pour uploader l'image de profil"""
    if request.method == 'POST':
        try:
            # Créer le dossier s'il n'existe pas
            image_folder = Path('static/images')
            image_folder.mkdir(parents=True, exist_ok=True)
            
            # Vérifier qu'un fichier est présent
            if 'file' not in request.files:
                return jsonify({'error': 'Pas de fichier uploadé'}), 400
            
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'Pas de fichier sélectionné'}), 400
            
            # Accepter seulement les images
            if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return jsonify({'error': 'Format non accepté. Utilisez JPG, PNG ou GIF'}), 400
            
            # Sauvegarder l'image
            filename = 'profile.jpg' if file.filename.lower().endswith(('.jpg', '.jpeg')) else 'profile.png'
            filepath = image_folder / filename
            file.save(filepath)
            
            return jsonify({'success': True, 'message': f'Image sauvegardée : {filename}'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # GET : afficher la page d'upload
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Upload Image de Profil</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
            }
            .container {
                border: 2px solid #667eea;
                padding: 30px;
                border-radius: 8px;
                text-align: center;
            }
            h1 {
                color: #667eea;
            }
            input[type="file"] {
                padding: 10px;
                margin: 20px 0;
            }
            button {
                background: #667eea;
                color: white;
                padding: 10px 30px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #764ba2;
            }
            .message {
                margin-top: 20px;
                padding: 15px;
                border-radius: 6px;
            }
            .success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📸 Upload Image de Profil</h1>
            <form id="uploadForm">
                <input type="file" id="fileInput" accept="image/*" required>
                <br>
                <button type="submit">Uploader</button>
            </form>
            <div id="message"></div>
        </div>
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData();
                formData.append('file', document.getElementById('fileInput').files[0]);
                
                try {
                    const response = await fetch('/upload-profile', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    const messageDiv = document.getElementById('message');
                    
                    if (response.ok) {
                        messageDiv.innerHTML = `<div class="message success">✅ ${data.message}<br><a href="/">Retour à l'accueil</a></div>`;
                    } else {
                        messageDiv.innerHTML = `<div class="message error">❌ ${data.error}</div>`;
                    }
                } catch (error) {
                    document.getElementById('message').innerHTML = `<div class="message error">❌ Erreur: ${error}</div>`;
                }
            });
        </script>
    </body>
    </html>
    '''


@app.route('/calculate', methods=['POST'])
def calculate():
    """API pour effectuer les calculs"""
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


# ========================
# ERROR HANDLERS
# ========================

@app.errorhandler(404)
def not_found(error):
    """Gère les erreurs 404"""
    return jsonify({'error': 'Page non trouvée'}), 404


@app.errorhandler(500)
def server_error(error):
    """Gère les erreurs 500"""
    return jsonify({'error': 'Erreur serveur'}), 500


# ========================
# MAIN
# ========================

if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=True
    )
