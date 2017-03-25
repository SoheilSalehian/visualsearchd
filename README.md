# visualsearchd
Visual search engine based on the inception model.

## Setup
1. Download the index by running:
`sh downloadModel.sh`

2. Build the docker container:

`docker build -t visualsearch .`

3. Run and forward port
`docker run -p 8000:8000 -it visualsearch`

4. Send query for example:
`curl -XPOST -d'{"image_url": "http://example.com/test.jpg"}' http://0.0.0.0:8000/search`
