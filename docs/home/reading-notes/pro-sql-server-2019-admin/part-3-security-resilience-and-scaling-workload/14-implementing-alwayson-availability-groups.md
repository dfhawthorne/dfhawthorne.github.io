---
layout: default
title: '14. Implementing Always On Availability Group'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/14-implementing-alwayson-availability-groups.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part III. Security Resilience and Scaling Workload'
  url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload
---

- Traditional on Windows Failover Cluster
- Linux Pacemaker
- 2017+ Cluster not needed for reporting but need one for HA, DR

[SQL Server Always On Revealed](https://www.oreilly.com/library/view/sql-server-alwayson/9781484217634/)

Recovery mode FULL

- SQL/Server Configuration manager
  - SQL/Server Services
    - Properties
      - Always On tab
        - Enable AOAG
        - Check cluster name

Restart server and repeat for each node

```powershell
Enable-SqlAlwaysOn -Path SQLSERVER:\SQL\CLUSTERNODE1\PRIMARYREPLICA
```

Take a full backup of all database in AG

Cluster type = NONE =\> Clusterless AG

"hardening the log" commit on secondary before primary.

- Sync - allows auto fail-over
- Async - commit on primary before secondary

default port for endpoint = 5022

Ensure same service account is used by all instances in a cluster else grant each service account instance privileges

Only one database mirroring endpoint per instance

- create login for service account
  - grant connect to endpoint

After creation of AG, create AG listener

## AG in Linux

```bash
sudo /opt/mssql/bin/mssql-conf set hadr.hadrenabled
sudo systemctl restart mssqk-server
```

Create certificates for server authentication through SQL/Server

```sql
CREATE ENDPOINT ...;
CREATE AVAILABILITY GROUP x
  CLUSTER TYPE=EXTERNAL;
```

Pacemaker

```sql
/* Primary */
ALTER AVAILABILITY GROUP x GRANT CREATE ANY DATABASE;
/* Replica */
ALTER AVAILABILITY GROUP x JOIN WITH (CLUSTER TYPE=EXTERNAL);
ALTER AVAILABILITY GROUP x GRANT CREATE ANY DATABASE;
/* Primary */
CREATE DATABASE y;
ALTER DATABASE y SET RECOVERY FULL;
BACKUP DATABASE y TO DISK ...;
ALTER AVAILABILITY GROUP x ADD DATABASE y;
ALTER AVAILABILITY GROUP x ADD LISTENER z (WITH IP((ip,mask)) PORT=p);
```

## Distributed Availabilty Groups

Allows for synchronisation between AG:

- between widows and Linux
- cross-site
- increases #replicas

`WITH (DISTRIBUTED)`

Databases will need to be manually joined to secondary replicas withon the secondary AG.

## Managing AOAG

```sql
ALTER AVAILABILITY GROUP x FAILOVER; /* Sync */
ALTER AVAILABILITY GROUP x FORCE_FAILOVER_ALLOW_DATA_LOSS; /* Async */
```

on new primary:

- Disable logins
- replicas sync
- Failover
- replica async
- enable logins

Use SSIS to synchronise uncontained objects such as logins, credentials, jobs, etc.

- _Always On Dashboard_ (SSMS) via _Object Explorer_
- _Always On Health Trace_
  - Extended event session (SSMS)

```sql
ALTER DATABASE x SET HADR OFF;
```

Suspended data movement prevents log truncation on primary:

```sql
SET HADR [SUSPEND|RESUME];
```

Same location for files on primary and replicas

Safe state cannot be single user or restricted for AG database.
