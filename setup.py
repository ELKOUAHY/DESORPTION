#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de configuration pour la plateforme de calcul
Crée la structure de dossiers et aide à configurer l'app
"""

import os
from pathlib import Path
import shutil

def setup_project():
    """Crée la structure du projet"""
    print("=" * 60)
    print("📦 Configuration de la plateforme de calcul de désorption")
    print("=" * 60)
    
    # Créer les dossiers
    folders = [
        'static/images',
        'static/css',
        'static/js',
        'templates'
    ]
    
    print("\n✓ Création des dossiers...")
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {folder}/")
    
    # Vérifier les fichiers
    print("\n✓ Vérification des fichiers...")
    
    required_files = {
        'app.py': 'Fichier principal Flask',
        'requirements.txt': 'Dépendances Python',
        'templates/accueil.html': 'Page d\'accueil',
        'templates/calcul.html': 'Page de calcul',
        'static/css/accueil.css': 'Styles d\'accueil',
        'static/css/calcul.css': 'Styles de calcul',
        'static/js/calcul.js': 'JavaScript de calcul',
    }
    
    for file, desc in required_files.items():
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MANQUANT!")
    
    # Image de profil
    print("\n✓ Status de l'image de profil:")
    image_files = list(Path('static/images').glob('profile.*'))
    if image_files:
        print(f"  ✓ Image trouvée: {image_files[0].name}")
    else:
        print(f"  ✗ Aucune image profile.jpg ou profile.png trouvée")
        print(f"    → placeholder.svg disponible en cas d'absence")
    
    # Instructions finales
    print("\n" + "=" * 60)
    print("🚀 Prêt à démarrer!")
    print("=" * 60)
    print("\n1️⃣  Installe les dépendances:")
    print("   pip install -r requirements.txt")
    print("\n2️⃣  Lance l'application:")
    print("   python app.py")
    print("\n3️⃣  Va sur:")
    print("   http://127.0.0.1:5000")
    print("\n4️⃣  Pour uploader l'image:")
    print("   http://127.0.0.1:5000/upload-profile")
    print("\n5️⃣  Pour voir la configuration:")
    print("   http://127.0.0.1:5000/setup")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    setup_project()
