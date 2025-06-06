FROM python:3.6.15-slim-buster

# Instala SoftHSM2 e outras dependências
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    softhsm2 \
    libtool \
    libssl-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*

# Instala a biblioteca Python pkcs11
RUN pip install python-pkcs11

# Cria diretório de configuração para SoftHSM
RUN mkdir -p /root/.config/softhsm2
COPY softhsm2.conf /root/.config/softhsm2/softhsm2.conf

# Define o working directory
WORKDIR /app
COPY . /app

CMD [ "python", "main.py" ]

