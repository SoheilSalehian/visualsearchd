package main

import (
	"fmt"
	"io"
	"net/http"
	"os"

	log "github.com/Sirupsen/logrus"
)

// Download the images for later indexing in vs
func downloadShopStyleImages(url string, productID int) {
	log.Info(productID)
	response, err := http.Get(url)
	if err != nil {
		log.Error(err)
	}

	defer response.Body.Close()

	fname := fmt.Sprintf("./shopstyle_images/%d.jpg", productID)
	file, err := os.Create(fname)
	if err != nil {
		log.Error(err)
	}

	_, err = io.Copy(file, response.Body)
	if err != nil {
		log.Error(err)
	}
	file.Close()
	log.Info("Download completed: ", fname)
}

func download(number int) {
	for i := 0; i < number; i++ {
		products, _ := callShopStyle(i * 50)
		for _, product := range products.Products {
			downloadShopStyleImages(product.Image.Sizes.Original.URL, product.ID)
		}
	}
}
