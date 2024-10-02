---
layout: default
title: '01. Planning the Deployment'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration/01_planning_the_deployment.html
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

## Editions and License Model

| Edition | License |
| --- | --- |
| Enterprise | per core |
| Standard | per core |
| | server plus CAL |
| Web | Third party hosting only |
| Developer | Free (non-production) |
| Express | Free (10GB for database, 1GB RAM, 4 cores) |

__CAL__ is _Client Access License__ (user or device).

| Edition | Options |
| --- | --- |
| Enterprise | All |
| Standard | Core plus BI |
| Web | Server providers for public web |
| Developer | All |
| Express | All |

Windows Server Core prevents:

- Report Server
- SQL Server Data Tools (SSDT)
- Client Tools Backward Compatible
- Client Tools SDK
- SQL Server Books online
- Distributed Replay Controller
- Master Data Servers (MDS)
- Data Quality Services (DQS)

Don't use `RAID0` for `TEMPDB` as loss of `TEMPDB` crashes the instance.

`RAID1` is better than `RAID10` for transaction logs. Not `RAID5`.

Data and log files on SAN. `TEMPDB` and buffer cache extensions should be locally attached -- SSD preferable.

Instead of placing data on disks, DBAs need to determine which SAN storage tier to use.

Write performance can be better than read ceause of write caches.

NTFS has a default blocksize of 4KB.

SQL/Server has a minimum extent of eight (8) 8KB blocks. Best performance can be achieved through setting blocksize to 64KB.

Use high performance power plan for database server.

Prioritise background over foreground as background processes are used by database instances.

Instant file initialisation:

- no zeroing out disk on allocation
- "Perform Volume Maintenance Tasks User Rights Assignment" granted to service account to enable

Lock pages in memory (EE|SE):

- grant "Lock Pages in Memory" to service account
- can interfere with balloon driver if on VM

SQL Audit to Security Log

