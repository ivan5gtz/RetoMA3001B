# Arguments
ARG PYTHON_VER="3.10"
FROM python:$PYTHON_VER

# Arguments
ARG PYTHON_VER="3.10"
ARG QUARTO_VER="1.3.450"
ARG ENV_NAME="OCR_fase1"

# Environment variables
ENV ENV_NAME=$ENV_NAME
ENV PYTHON_VER=$PYTHON_VER
ENV QUARTO_VER=$QUARTO_VER

RUN apt-get update \
  && apt-get -y install tesseract-ocr \ 
  && apt-get -y install libtesseract-dev \
  && apt-get -y install poppler-utils \
  && apt-get -y install unoconv \
  && apt-get -y install antiword

# Copy files
RUN mkdir requirements

COPY install_quarto.sh install_dependencies.sh requirements/
RUN bash ./requirements/install_dependencies.sh
RUN bash ./requirements/install_quarto.sh $QUARTO_VER

#RUN mkdir /app
#RUN git clone https://github.com/abetlen/llama-cpp-python.git /app
#WORKDIR /app
#RUN git submodule update --init --recursive

WORKDIR /

# Install dependencies
COPY requirements.txt install_requirements.sh requirements/
RUN bash requirements/install_requirements.sh $ENV_NAME $PYTHON_VER