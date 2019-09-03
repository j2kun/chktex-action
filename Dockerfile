FROM debian:buster

LABEL "com.github.actions.name"="LaTeX linter (chktex)"
LABEL "com.github.actions.description"="Detect stylistic errors in a LaTeX document"
LABEL "com.github.actions.icon"="edit"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="http://github.com/j2kun/chktex-action"
LABEL "homepage"="http://github.com/j2kun"
LABEL "maintainer"="Jeremy Kun <j2kun@users.noreply.github.com>"

WORKDIR /usr/src/app
RUN apt update
RUN apt install -y chktex python3.7 python3-pip

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./run_action.py" ]
