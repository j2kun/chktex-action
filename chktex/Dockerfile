FROM dockershelf/latex:basic

LABEL "com.github.actions.name"="LaTeX linter (chktex)"
LABEL "com.github.actions.description"="Detect mistakes in a LaTeX document"
LABEL "com.github.actions.icon"="edit"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="http://github.com/j2kun/latex-lint-action"
LABEL "homepage"="http://github.com/j2kun"
LABEL "maintainer"="Jeremy Kun <j2kun@users.noreply.github.com>"

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
