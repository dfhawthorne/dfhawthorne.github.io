---
layout: default
title: '16. Scaling Workloads'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/16-scaling-workloads.html
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

Database Snapshot Copy on Write:

- increases I/O load and memory footprint
- need to refresh snapshot regularity

Snapshot files `.ss` (preferred) or `.mdf` (alternate)

```sql
CREATE DATABASE db1
  ON PRIMARY (
    NAME='name',
    FILENAME='db.ss'
  )
  AS SNAPSHOT OF db2;
```

## Replication

- __Snapshot__:
  - `SnapshotAgent` (on Publisher) creates a system view and stored procedure before bulk copying to snapshot database. High overhead.
- __Transactional__:
  - Transactions are replicated to subscriber
  - `LogReaderAgent` (on Publisher)
  - VLF cannot be truncated until all needed transactions have been replicated
  - Peer-to-peer replication possible
    - Need to think about conflicts
    - `OriginatorID`
- __Merge__:
  - `rowguid` on every replicated table
  - unique identifier
  - Multiple conflict resolution

Need _SQL Server Agent_ active

`SnapshotAgent`:

- Database server for distributed database
- Read, write, modify on file server

`LogReaderAgent`:

- `db_owner` for distributed database

Sync type not auto require `sysadmin`

`DistributionAgent` account

- `db_owner` for distributed database
- Publication access list 
- Read on file share

Subscriber Account (`db_owner` for suscriber database)

All done through Wizard

## Adding Always-On Readable Secondary Replicas

> The main risk of using readable secondary replicas is that implementing snapshot isolation on the secondary replica can actually cause deleted records not to be cleaned up on the primary replica. This is because the ghost record cleanup task only removes rows from the primary once they are no longer required on the secondary.

- Can also delay log tuncation
- May need to kill long running queries on the secondary

2016+ Load balance R/O request
