FROM ubuntu:latest AS builder

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
    sed -i '/^install:/ s/ ChkTeX.dvi//' Makefile; \
    make install

FROM python:alpine

LABEL com.github.actions.name="ChkTeX Action"
LABEL com.github.actions.description="Lint your LaTeX files with ChkTeX"
LABEL com.github.actions.icon="edit"
LABEL com.github.actions.color="yellow"
LABEL repository="https://github.com/j2kun/chktex-action"
LABEL homepage="https://github.com/j2kun"
LABEL maintainer="Jeremy Kun <j2kun@users.noreply.github.com>"

COPY --from=builder /usr/local/bin/chktex /usr/local/bin/
COPY --from=builder /usr/local/etc/chktexrc /usr/local/etc/
COPY run_action.py /usr/src/chktex-action/
COPY entrypoint.sh /

RUN set -eux; \
    \
    apk add --no-cache \
    gcompat
