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
`uv run main.py` pour lancer la boucle de lecture/ouverture

`uv run main.py refresh` pour mettre à jour la liste des GHs

### Installation
```shell
make prod
```
`make prod` crée le `.venv` in-project et installe les dépendances depuis `uv.lock`.

Puis declarer deux services et un timer dans systemd. Ils sont dans le répertoire `./systemd`.

### Développement
```shell
make dev
```
