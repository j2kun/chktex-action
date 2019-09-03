FROM debian:jessie

LABEL "com.github.actions.name"="LaTeX linter (chktex)"
LABEL "com.github.actions.description"="Detect stylistic errors in a LaTeX document"
LABEL "com.github.actions.icon"="edit"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="http://github.com/j2kun/chktex-action"
LABEL "homepage"="http://github.com/j2kun"
LABEL "maintainer"="Jeremy Kun <j2kun@users.noreply.github.com>"

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y chktex python3 python3-pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run_action.py" ]
