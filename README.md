# Plateforme de Calcul de Désorption

Application Flask pour calculer les paramètres de désorption avec interface web moderne.

## Structure du Projet

```
e/
├── app.py                      # Application Flask principale
├── setup.py                    # Script de configuration
├── run.bat                     # Script de démarrage (Windows)
├── requirements.txt            # Dépendances Python
├── README.md                   # Ce fichier
│
├── templates/                  # Fichiers HTML
│   ├── accueil.html          # Page d'accueil
│   └── calcul.html           # Page de calcul
│
└── static/                     # Fichiers statiques
    ├── images/               # Images
    │   ├── profile.jpg       # Photo de profil (à uploader)
    │   └── placeholder.svg   # Image par défaut
    ├── css/                  # Feuilles de style
    │   ├── accueil.css       # Styles de la page d'accueil
    │   └── calcul.css        # Styles de la page de calcul
    └── js/                   # Scripts JavaScript
        └── calcul.js         # Logique de la page de calcul
```

## Installation rapide (Windows)

### Méthode 1️⃣ : Double-clic (le plus simple)

```
Double-clic sur run.bat
```

C'est tout ! L'app démarre automatiquement.

### Méthode 2️⃣ : Terminal PowerShell

```powershell
cd c:\Users\elkou\Downloads\e
python setup.py
pip install -r requirements.txt
python app.py
```

## 📸 Configuration de l'image de profil

### Option 1 : Interface web (recommandé)
1. Lance l'application
2. Va sur : **http://127.0.0.1:5000/upload-profile**
3. Clique sur "Choisir un fichier" et sélectionne ta photo
4. Clique sur "Uploader"
5. L'image s'affiche instantanément !

### Option 2 : Manuel
1. Enregistre ta photo en tant que `profile.jpg`
2. Place-la dans : `c:\Users\elkou\Downloads\e\static\images\`
3. Lance l'app et rafraîchis la page

### Option 3 : Voir le status
Va sur : **http://127.0.0.1:5000/setup**

Cela te montre :
- ✓ Status de la configuration
- ✓ Si l'image est présente
- ✓ Les dossiers créés

## 🚀 Démarrage de l'application

### Windows (double-clic)
```
run.bat
```

### Terminal
```powershell
python app.py
```

Puis ouvre : **http://127.0.0.1:5000**

## ✨ Routes disponibles

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil |
| `/calcul` | Page de calcul |
| `/upload-profile` | Upload l'image de profil |
| `/get-profile-image` | Endpoint pour servir l'image |
| `/setup` | Page de configuration |
| `/calculate` (POST) | API pour les calculs |

## 📊 Fonctionnalités

✅ **Page d'accueil** : Design professionnel avec image de profil  
✅ **Page de calcul** : Calculs scientifiques en temps réel  
✅ **Upload d'image** : Interface web pour télécharger la photo  
✅ **Graphiques** : Visualisation avec Chart.js  
✅ **Export CSV** : Téléchargement des résultats  
✅ **Responsive** : Fonctionne sur desktop et mobile  
✅ **Performance** : Mesure du temps d'exécution et mémoire

## 🛠️ Technos utilisées

- **Backend** : Python, Flask
- **Frontend** : HTML5, CSS3, JavaScript (ES6+)
- **Graphiques** : Chart.js
- **Librairies Python** : NumPy, Pandas, Psutil

## 📝 Configuration

Le serveur Flask est configuré pour :
- Servir les fichiers statiques depuis `static/`
- Servir les templates depuis `templates/`
- Écouter sur `127.0.0.1:5000`
- Mode debug activé pour le développement

## 🔧 Dépannage

### L'image n'apparaît pas ?
1. Va sur `/upload-profile` et réupload ta photo
2. Ou place ton image dans `static/images/profile.jpg`
3. Rafraîchis la page (Ctrl+F5 pour vider le cache)

### Erreur "Port déjà utilisé" ?
Le port 5000 est occupé. Arrête l'autre application ou utilise un autre port dans `app.py`

### Erreur "Module not found" ?
```powershell
pip install -r requirements.txt
```

## 📄 Notes de développement

- Utiliser `python app.py` pour tester en local
- Les modifications HTML/CSS/JS sont visibles au rafraîchissement
- Les modifications de `app.py` nécessitent un redémarrage
- Les logs Flask s'affichent dans le terminal
- Utiliser `python setup.py` pour recréer la structure des dossiers
