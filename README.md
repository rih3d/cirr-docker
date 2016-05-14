# CIRR UP!

Derek Merck <derek_merck@brown.edu>
Rhode Island Hospital

Spins up a Docker-based open source medical imaging informatics platform.  Originally developed to support the RIH Clinical Imaging Research Repository (CIRR).


### Services

- Log Monitoring - [Splunk] Lite on 2080 (HTTP), 2081 (REST), 2514 (syslog)
- Database - [Postgresql] on 3432 (SQL)
- Clinical/PHI Facing Receiver - [Orthanc] on 4080 (HTTP/REST), 4042 (DICOM)
- Clinical/PHI Facing Repository - Orthanc on 4081 (HTTP/REST), 4043 (DICOM)
- Research/Anonymized Facing Repository - [XNAT] 1.6.5 on 5080 (HTTP), 5042 (DICOM), ??? (REST)
- Data Orchestration - [Tithonus] on 6080 (HTTP)

[Splunk]:(http://www.splunk.com)
[Postgresql]:(http://www.postgresql.org)
[Orthanc]:(http://www.orthanc-server.com)
[XNAT]:(http://www.xnat.org)
[Tithonus]:()


## Dependencies

- [Docker], [docker-compose] for service virtualization
- [Python] 2.7, [pyyaml], [jinja2] for `bootstrap.py`

[Docker]:
[docker-compose]:
[Python]:
[pyyaml]:
[jinja2]:


## Configurations

Warning: once data has been ingested, do _not_ use `docker-compose down`, or you will drop the data volume!


### Orthanc w Postgres and Persistent Compressed Data Storage

```bash
$ python bootstrap.py orthanc  # Sets up orthanc.json from template, adds db
$ docker-compose up orthanc
```

Orthanc with receiver proxy:

```bash
$ python bootstrap.py orthanc orthanc-receiver
$ docker-compose up orthanc-reciever
```

The additional DICOM receiver can be used as a proxy to accept DICOM transfers and queue them for the main clinical-facing repository.  The main repo slows down considerably as the DB grows large, particularly if compression is on.[^orthanc_speed]

[^orthanc_speed]:  On a reasonable machine, we measured about 20 images/second in an empty, uncompressed repo, about 1.5 scans/sec in a repo w 100k instances and compression on.


### XNAT w Postgres and Persistent Data Storage

```bash
$ python bootstrap.py xnat    # Initializes config from template, creates image, drops db if it exists
$ docker-compose up xnat
```


### XNAT and Orthanc with a Tithonus Gatekeeper

```bash
$ python bootstrap.py orthanc xnat
$ docker-compose up orthanc xnat tithonus
```

[Tithonus] can be configured to automatically move data from clinical DICOM sources into the clinical facing receiver, and from the clinical repository or other sources into the anonymized research-facing repository.


### XNAT and Orthanc with a Splunk Log Handler

```
$ python bootstrap.py orthanc xnat
$ docker-compose up orthanc xnat splunk
```


### Complete CIRR Configuration

```bash
$ python bootstrap.py orthanc orthanc-receiver xnat
$ docker-compose up
```


### Administration

To inspect the data or logs, mount the data volume on another container.

```
$ docker-compose up -f docker-compose.admin.yml admin
```

Or manually for a single service:

```bash
$ docker-compose run -it --volumes-from orthanc --volumes-from postgres --volumes-from xnat ubuntu /bin/bash
```

To perform a data backup, run `admin` or otherwise mount the volumes and use `tar`.

```bash
$ docker-compose run -f docker-compose.admin.yml admin tar zcvf /backup/postgres.tar.gz /var/lib/postgresql/data
$ docker-compose run -f docker-compose.admin.yml admin tar zcvf /backup/xnat.tar.gz /var/lib/xnat/data
```


## Acknowledgements

Uses Docker images from:

- [jodogne/orthanc]: https://github.com/jodogne/OrthancDocker
- [chaseglove/xnat]: https://github.com/chaselgrove/xnat-docker
- [outcoldman/splunk]:https://github.com/outcoldman/docker-splunk


## Note

Run this command to configure your shell to use docker-compose:

```
$ eval "$(docker-machine env default)"
```

## License

MIT
