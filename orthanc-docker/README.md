# Docker composition for Orthanc with Postgres and persistent data storage

## Usage
```
$ export DB_ORTHANC_USER="orthanc"; export DB_ORTHANC_PASSWORD="orthanc"; 
$ ./bootstrap-config.sh
$ docker-compose up postgres # Allow it to initialize and kill it
$ docker compose up
```

To inspect the data or logs, mount the data volume on another container.

```
$ docker run -it --volumes-from orthancdocker_orthanc_1 --volumes-from orthancdocker_postgres_1 ubuntu /bin/bash
```

To do a backup, mount the volume and use `tar`.

```
$ docker run --rm --volumes-from orthancdocker_postgres_1 -v $(pwd):/backup ubuntu tar zcvf /backup/backup.tar.gz /var/lib/postgresql/data
```