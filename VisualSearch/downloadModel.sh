#!/bin/bash
aws s3 cp s3://${INDEX_BUCKET_NAME}/ index/ --recursive
