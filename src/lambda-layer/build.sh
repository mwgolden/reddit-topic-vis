#!/usr/bin/env bash
set -e

LAYER_NAME=reddit_data_dependencies
PYTHON_VERSION=python3.12

mkdir -p build/lambda-layer/python/lib/${PYTHON_VERSION}/site-packages

pip install \
    --platform manylinux2014_x86_64 \
    --only-binary=:all: \
    --implementation cp \
    --python-version 312 \
    --target build/lambda-layer/python/lib/${PYTHON_VERSION}/site-packages \
    -r src/lambda-layer/requirements.txt

cd build/lambda-layer
zip -r ../reddit-data-dependencies.zip .
cd ../..