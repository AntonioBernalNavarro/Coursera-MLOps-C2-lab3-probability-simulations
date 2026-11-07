# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/codespaces-linux/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/universal:2-focal

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# Elimina la fuente APT de Yarn que causa el error 100
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Actualiza e instala todas las dependencias necesarias con reintentos
RUN apt-get update -o Acquire::Retries=5 \
    && apt-get install -y --no-install-recommends ca-certificates \
    && apt-get update -o Acquire::Retries=5 \
    && apt-get install -y --no-install-recommends \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
    && rm -rf /var/lib/apt/lists/*
