# Utilise l'image de base Python
FROM python:3.12-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie le fichier requirements.txt et installe les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port 8000
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
