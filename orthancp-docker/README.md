# ORTHANC UP!

Derek Merck <derek_merck@brown.edu>
Rhode Island Hospital

Configures and spins up a Docker-based Orthanc instance with a Postgres backend.

## Requirements

Set environment variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DB_USER`, and `DB_PASSWORD`.

## Usage

```bash
$ ./bootstrap-orthanc.sh
$ docker-compose up
```