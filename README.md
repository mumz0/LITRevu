# LITRevu

LITRevu est une application web de critique littéraire développée avec Django. Elle permet aux utilisateurs de demander et publier des critiques de livres et d'articles.

## Fonctionnalités

- **Authentification** : Inscription et connexion des utilisateurs
- **Gestion des tickets** : Demander des critiques pour des livres/articles
- **Système de critiques** : Publier des critiques avec notes (0-5 étoiles)
- **Abonnements** : Suivre d'autres utilisateurs pour voir leurs publications
- **Flux personnalisé** : Voir les publications des utilisateurs suivis
- **Interface responsive** : Design moderne avec Tailwind CSS

## Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

## Installation et Configuration

### 1. Cloner le projet

```bash
git clone <url-du-repository>
cd LITRevu
```

### 2. Créer un environnement virtuel

**Windows :**
```bash
python -m venv env
```

**macOS/Linux :**
```bash
python3 -m venv env
```

### 3. Activer l'environnement virtuel

**Windows (PowerShell) :**
```powershell
.\env\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
env\Scripts\activate.bat
```

**Windows (Git Bash) :**
```bash
source env/Scripts/activate
```

**macOS/Linux :**
```bash
source env/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configuration de la base de données

Naviguer dans le répertoire du projet Django :
```bash
cd litrevu
```

Appliquer les migrations :
```bash
python manage.py migrate
```

### 6. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000/`

## Technologies Utilisées

- **Backend** : Django 5.0.2
- **Frontend** : HTML5, Tailwind CSS 2.1.2
- **Base de données** : SQLite
- **Gestion d'images** : Pillow
- **Icônes** : Font Awesome Free

## Dépannage

### Problèmes courants

**Erreur "Unable to create process using python.exe"**
- Recréez l'environnement virtuel dans le bon répertoire

**Erreur d'installation de Pillow**
```bash
pip install --upgrade pip
pip install pillow
```

**Messages Django non affichés**
- Vérifiez que `django.contrib.messages` est dans `INSTALLED_APPS`
- Assurez-vous que le context processor des messages est activé

### Réinitialiser la base de données

```bash
cd litrevu
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```
