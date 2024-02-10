FROM postgres:15.4-alpine3.18
MAINTAINER ChengTze Wu <chengtzewu@gmail.com>

# Dependencies for system_stats
RUN apk update && \
    apk add --no-cache clang15 llvm15 make gcc musl-dev wget

# install system_stats downloaded from https://github.com/EnterpriseDB/system_stats/releases/tag/v2.1
WORKDIR /lib/tmp
RUN wget https://github.com/EnterpriseDB/system_stats/archive/refs/tags/v2.1.tar.gz && \
    tar -zxvf v2.1.tar.gz && \
    cd system_stats-2.1 && \
    PATH="/usr/local/pgsql/bin:$PATH" make USE_PGXS=1 && \
    PATH="/usr/local/pgsql/bin:$PATH" make install USE_PGXS=1 && \
    rm -rf /lib/tmp

WORKDIR /

EXPOSE 5432