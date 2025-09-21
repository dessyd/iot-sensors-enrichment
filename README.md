# IoT Sensors Enrichment

API FastAPI pour la gestion et l'enrichissement de devices IoT.

Variables d'environnement requises

- DATABASE_URL ou SQLITE_FILE : chemin/URL sqlite (ex: sqlite:///./data.db)
- ADMIN_PASSWORD : mot de passe initial pour l'utilisateur admin
- JWT_SECRET : secret pour signer les tokens JWT
- JWT_ALGORITHM : algorithme (ex: HS256)
- JWT_EXPIRATION : durée en minutes pour l'expiration du token (ex: 60)

Initialisation

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Exporter les variables d'environnement :

```bash
export ADMIN_PASSWORD="changeme"
export JWT_SECRET="supersecret"
export DATABASE_URL="sqlite:///./iot.db"
```

Env & helper

Pour simplifier la configuration locale, copiez le fichier d'exemple et utilisez le script fourni :

```bash
# copier l'exemple et éditer si besoin
cp .env.example .env

# ou générer un .env sécurisé (génère un JWT_SECRET fort)
./scripts/generate_env.sh
```

Le fichier `.env` est ajouté à `.gitignore` par défaut afin d'éviter de pousser des secrets.

3. Initialiser la base de données et créer l'utilisateur admin :

```python
from app.db import init_db
from app.db import engine
from app.models import User
from app.auth import get_password_hash

init_db()
# connectez-vous via un shell pour créer l'utilisateur admin si nécessaire
```

Démarrer le serveur

```bash
uvicorn main:app --reload
```

Exemples d'appels

- Obtenir un token :

```bash
curl -X POST -F "username=admin" -F "password=changeme" http://127.0.0.1:8000/auth/token
```

- Lister les devices :

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/devices
```

- Obtenir un device :

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/devices/device123
```

- Import CSV :

```bash
curl -X POST -H "Authorization: Bearer <token>" -F "file=@devices.csv" http://127.0.0.1:8000/devices/csv
```

- Export CSV :

```bash
curl -H "Authorization: Bearer <token>" "http://127.0.0.1:8000/devices/csv?path=/tmp/devices.csv"
```

Format CSV attendu

device_id,name,location,model,metadata_json

Exemples

```csv
device123,Boiler,BoilerRoom,ModelX,{"firmware":"1.2","capabilities":["temp","pressure"]}
```


## Sécurité des tokens (JWT_SECRET)

La variable d'environnement `JWT_SECRET` est la clé utilisée pour signer
et vérifier les JSON Web Tokens (JWT) émis par l'application. Elle
garantit l'intégrité et l'authenticité des tokens : si un attaquant connaît
cette clé, il peut forger des tokens valides (se faire passer pour
n'importe quel utilisateur, y compris `admin`).

Bonnes pratiques

- Générer une clé forte (ex : 32 octets aléatoires encodés en base64).
- Ne pas committer `JWT_SECRET` dans le dépôt. Utiliser `.env` (ignoré par
	git) pour le développement, et un gestionnaire de secrets en production
	(AWS Secrets Manager, HashiCorp Vault, etc.).
- Garder une durée d'expiration courte via `JWT_EXPIRATION` pour limiter la
	fenêtre d'exploitation si une clé fuit.
- Pour une sécurité accrue, envisagez RS256 (clé privée/publique) afin de
	séparer signature et vérification.

Générer une clé sécurisée (exemples)

```bash
# openssl (32 bytes base64)
openssl rand -base64 32

# python (venv)
.venv/bin/python - <<'PY'
import secrets, base64
print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())
PY
```

Ajout dans `.env`

```text
# ne pas committer ce fichier
JWT_SECRET="<valeur_générée>"
JWT_ALGORITHM=HS256
JWT_EXPIRATION=60
```

