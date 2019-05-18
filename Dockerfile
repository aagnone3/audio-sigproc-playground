FROM tensorflow/magenta

VOLUME /opt
WORKDIR /opt

RUN apt-get update && apt-get install -y --fix-missing \
    vim \
    tmux \
    screen \
    git \
    python-pip \
    portaudio19-dev

# python packages
# install numpy before anything to ensure the desired version is used
RUN pip install --upgrade pip
RUN pip install \
    numpy \
    scipy \
    jupyterlab \
    torch \
    torch-vision \
    seaborn \
    scikit-learn \
    matplotlib \
    librosa \
    pyaudio \
    aubio
