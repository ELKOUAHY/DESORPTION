@echo off
REM Script de démarrage pour Windows
REM Lance l'application Flask

title Plateforme de Calcul de Desorption
cd /d "%~dp0"

echo.
echo ======================================
echo Plateforme de Calcul de Desorption
echo ======================================
echo.

REM Vérifie si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur: Python n'est pas installé ou n'est pas dans PATH
    pause
    exit /b 1
)

echo [1/3] Configuration du projet...
python setup.py

echo.
echo [2/3] Installation des dépendances...
pip install -q -r requirements.txt

echo.
echo [3/3] Démarrage de l'application...
echo.
echo Votre application est prête!
echo.
echo Ouvre ton navigateur:
echo http://127.0.0.1:5000
echo.
echo Pour uploader l'image:
echo http://127.0.0.1:5000/upload-profile
echo.
echo Appuie sur Ctrl+C pour arrêter le serveur
echo.

python app.py

pause
