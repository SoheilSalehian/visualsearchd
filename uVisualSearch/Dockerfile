FROM gcr.io/tensorflow/tensorflow:latest

RUN apt-get update && apt-get install -y protobuf-compiler \
    python-scipy \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libssl-dev libffi-dev
RUN pip install --upgrade pip \
                          nearpy \
                          awscli \
                          flask \
                          requests \
                          boto3 \
                          protobuf \
                          humanize
RUN apt-get update && apt-get install -y git \
    unzip \
    && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY . /app
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["app.py"]
