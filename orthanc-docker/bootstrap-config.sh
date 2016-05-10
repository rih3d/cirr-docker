#!/usr/bin/env bash

export DB_HOST="postgres"
export DB_NAME="orthanc"

cat orthanc.template.json \
        | sed "s|%DB_HOST%|${DB_HOST}|" \
        | sed "s|%DB_NAME%|${DB_NAME}|" \
        | sed "s|%DB_USER%|${POSTGRES_CIRR_USER}|" \
        | sed "s|%DB_PASSWORD%|${POSTGRES_CIRR_PASSWORD}|" \
        > orthanc.shadow.json
