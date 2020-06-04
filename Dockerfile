FROM ubuntu:16.04

ARG PYTHON_VERSION=3.6

RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         ca-certificates \
         libjpeg-dev \
         libpng-dev \
         vim \
         wget && \
     rm -rf /var/lib/apt/lists/*

RUN  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh -nv -q && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION && \
     /opt/conda/bin/conda clean -ya

ENV PATH /opt/conda/bin:$PATH
WORKDIR /code

RUN git clone https://github.com/CosmiQ/solaris.git && \
    cd solaris && \
    conda env create -n solaris -f environment.yml

RUN echo "source activate solaris" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

RUN /bin/bash -c "source activate solaris && \
    cd solaris && \
    pip install -e ."

COPY . .
RUN /bin/bash -c "source activate solaris && \
    pip install -e . && \
    conda install -c conda-forge notebook"
