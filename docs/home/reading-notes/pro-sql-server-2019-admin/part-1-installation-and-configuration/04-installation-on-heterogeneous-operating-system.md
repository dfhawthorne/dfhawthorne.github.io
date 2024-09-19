---
layout: default
title: '04. Installation on Heterogeneous Operating Systems'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration/04-installation-on-heterogeneous-operating-system.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part I. Installation and Configuration'
  url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration.html
---

- RHEL 7.5+
- SUSE V12SP2
- Ubuntu 16.4

```bash
systemctl restart mssql-server
mssql-cli
```

Containers are stateless

```bash
docker run \
    -d \
    -p 1433-1433 \
    -e sas_password=... \
    -e ACCEPT_EULA=Y \
    <container>
```

Kubernetes is a container orchestrator

Big Data clusters

Can build an <em>Availability Group</em> inside Kubernetes.

