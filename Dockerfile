FROM python:3.9

RUN apt-get update && \
    apt-get install -y vim git && \
    apt-get install -y software-properties-common && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y git-lfs

RUN useradd -ms /bin/bash myuser

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

USER myuser

CMD ["/bin/bash"]

