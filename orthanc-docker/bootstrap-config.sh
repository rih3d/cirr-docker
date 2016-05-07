#!/usr/bin/env bash

export DB_HOST="db"
export DB_ORTHANC_NAME="orthanc"

cat orthanc.json.template \
        | sed "s|%DB_HOST%|${DB_HOST}|" \
        | sed "s|%DB_ORTHANC_NAME%|${DB_ORTHANC_NAME}|" \
        | sed "s|%DB_ORTHANC_USER%|${DB_ORTHANC_USER}|" \
        | sed "s|%DB_ORTHANC_PASSWORD%|${DB_ORTHANC_PASSWORD}|" \
        > shadow.orthanc.json