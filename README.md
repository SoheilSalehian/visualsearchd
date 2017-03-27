# visualsearchd
Visual search engine based on the inception model.

## Setup
1. Download the index by running:
`cd uVisualSearch && sh downloadModel.sh`

2. Run docker-compose in the root directory:
`docker-compose build && docker-compose up`

3. Send query for example:
`curl -XPOST -d'{"image_url": "http://example.com/test.jpg"}' http://0.0.0.0:8000/search`
