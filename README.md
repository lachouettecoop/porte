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
`python3 main.py` pour lancer la boucle de lecture/ouverture

`python3 main.py refresh` pour mettre à jour la liste des GHs

### Installation
```shell
pip install -r requirements.txt
```
Puis declarer deux services et un timer dans systemd. Ils sont dans le répertoire `./systemd`.

### Développement
```shell
make dev
```
