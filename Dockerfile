FROM ubuntu:latest AS chktex_builder

ENV CHKTEX_VERSION=1.7.9

RUN set -eux; \
    \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y \
    build-essential \
    libpcre2-posix3 \
    libpcre2-dev \
    curl \
    ; \
    cd tmp/; \
    curl -sLO http://download.savannah.gnu.org/releases/chktex/chktex-${CHKTEX_VERSION}.tar.gz; \
    tar -xzf chktex-${CHKTEX_VERSION}.tar.gz; \
    cd chktex-${CHKTEX_VERSION}/; \
    ./configure; \
    make; \
    # Disable the documentation building
    sed -i '/^install:/ s/ ChkTeX.dvi//' Makefile; \
    make install

FROM python:alpine AS development

WORKDIR /usr/src/chktex-action/

COPY poetry.lock poetry.toml pyproject.toml README.md ./
COPY --from=chktex_builder /usr/local/bin/chktex /usr/local/bin/
COPY --from=chktex_builder /usr/local/etc/chktexrc /usr/local/etc/

RUN set -eux; \
    \
    apk add --no-cache \
    gcompat \
    ; \
    python3 -m pip install --root-user-action ignore --no-cache-dir --upgrade \
    pip \
    poetry \
    poetry-plugin-export \
    ; \
    poetry install

FROM development AS production_builder

RUN poetry export --without-hashes -o requirements.txt

FROM python:alpine

LABEL com.github.actions.name="ChkTeX Action"
LABEL com.github.actions.description="Lint your LaTeX files with ChkTeX"
LABEL com.github.actions.icon="edit"
LABEL com.github.actions.color="yellow"
LABEL repository="https://github.com/j2kun/chktex-action"
LABEL homepage="https://github.com/j2kun"
LABEL maintainer="Jeremy Kun <j2kun@users.noreply.github.com>"

WORKDIR /usr/src/chktex-action/

COPY --from=chktex_builder /usr/local/bin/chktex /usr/local/bin/
COPY --from=chktex_builder /usr/local/etc/chktexrc /usr/local/etc/
COPY --from=production_builder /usr/src/chktex-action/requirements.txt ./

RUN set -eux; \
    \
    apk add --no-cache \
    gcompat \
    ; \
    python3 -m pip install --root-user-action ignore --no-cache-dir \
    -r requirements.txt

COPY src/ src/

# The GitHub runner uses --workdir, so the absolute path has to be used
CMD ["python3", "/usr/src/chktex-action/src/chktex_action/main.py"]
