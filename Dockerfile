FROM ubuntu:mantic

LABEL "com.github.actions.name"="LaTeX linter (chktex)"
LABEL "com.github.actions.description"="Detect stylistic errors in a LaTeX document"
LABEL "com.github.actions.icon"="edit"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="http://github.com/j2kun/chktex-action"
LABEL "homepage"="http://github.com/j2kun"
LABEL "maintainer"="Jeremy Kun <j2kun@users.noreply.github.com>"

WORKDIR /tmp/action

COPY requirements.txt .

RUN apt-get update -yqq && \
  apt-get install -yqq \
  chktex \
  python3.7 \
  python3-pip && \
  rm -rf /var/lib/apt/lists/* && \
  pip3 install --break-system-packages -r requirements.txt

COPY . .

CMD [ "python3", "/tmp/action/run_action.py" ]
