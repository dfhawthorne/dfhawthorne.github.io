---
layout: default
title: '13. High Availability and Disaster Recovery Concepts'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/13-high-availability-and-disaster-recovery-concepts.html
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

- _Hot Failover_: Clustering, Always On Availability Group (synchronous) - High Availabilty
- _Warm Failover_: Log shipping, Always On Availability Group (asynchronous) - disaster recovery
- _Cold_: unsynchronous

## Always On Failover Clustering

Up to 64 servers. Always On Failover Clustered Instance. FCI. Single site. Shared storage. One server owns the FCI. Active node.

Windows Storage Replica (2016+) geoclusters

VIP is assigned to active instance. Application servers connect to VIP

- Active/Passive
- Active/Active - multiple instances in a cluster. Instances can move between nodes within a cluster.

Quorum may include a witness device

Authorative partition `/fq`

Quorum models:

- Node majority - odd number of nodes
- Node plus Disk Witness Majority
- Node plus file share witness majority - avoids VM issues with shared disk

Can change Node Weight to zero

Dynamic Quorum - Tie Breaker

## Always On Availability Groups (AOAG)

AOAG = Database mirroring plus cluster - stand alone instances

Needs availability group listener installed on the cluster

AOAG - best for small database with low write profiles - allows for synchronous commits on all nodes (HA). Up to 8 replicas implies a 9 node cluster including 3 synchronous replicas

AOAG (DR) - asynchronous mode

Failover at level of AG. Multiple AG per instance. Maximum (100 database amd 10 AG) per instance (Microsoft recommendation)

One database mirroring and point per instance - all log streams go through this i/p

Each AG has its own network name and IP address

Application reconnects after failover

## Automatic Page Repair

Good page gotten from a replica except - file header, database boot, allocation

## Log Shipping

Backup transaction log on primary, ship to secondary; restore it

## Recovery Modes

- recovery brings database online - not supported for log shipping
- norecovery keeps database offline to allow more backup to be applied - normal for log shipping
- standby bring database online as R/O
- can restore further backup
  - TUF (Transaction Undo File)

## Remote Monitor Server

- needs to be configured with log shipping
- cannot be added to an existing log shipping configuration

Failover - backup tail log; copy remaining backup; apply them in order; last one with `RECOVERY`

Can combine AOFOC with AOAG

- AOFOC HA
- AOAG DR and/or reporting

Synchronous mode allows automatic failover. Asynchronous mode only allows manual failover.

Can combine AOFOC with log shipping
