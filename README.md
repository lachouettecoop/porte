# porte
Ouverture de la porte via la scanette

### Utilisation
Créer un fichier config.yaml :
```yaml
default_gh_list:  # Liste des codes barres par default
  - "123"
  - "456"

sentry:           # Configuration du DSN sentry
  dsn: "https://foo.bar"

push_test_urls:
  - https://push.statuscake.com/...
```
`python main.py` pour lancer la boucle de lecture/ouverture

`python main.py refresh` pour mettre à jour la liste des GHs

### Installation
```shell
pip install poetry
poetry export --without-hashes --format=requirements.txt > requirements.txt
pip install -r requirements.txt
```
Puis declarer deux services et un timer dans systemd. Ils sont dans le répertoire `./systemd`.

### Développement
```shell
pyenv install 3.7.16
pyenv global 3.7.16
pip install poetry
poetry install
pre-commit install-hooks
```
