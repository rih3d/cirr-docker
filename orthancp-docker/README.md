# ORTHANC UP!

Derek Merck <derek_merck@brown.edu>
Rhode Island Hospital

Spins up a Docker-based Orthanc instance with a Postgres backend.

### Requirements

Set environment variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_CIRR_USER`, and `POSTGRES_CIRR_PASSWORD`.

### Usage

```bash
$ ./bootstrap-orthanc.sh
$ docker-compose up
```