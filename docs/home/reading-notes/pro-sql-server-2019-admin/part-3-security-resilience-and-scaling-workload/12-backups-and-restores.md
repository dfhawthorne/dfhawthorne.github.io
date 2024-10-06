---
layout: default
title: '12. Backups and Restores'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/12-backups-and-restores.html
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

- __SIMPLE__: Low overhead, RPO is last backup. Log truncation is done at `CHECKPOINT`.
- __FULL__: Log truncated after log backup and `CHECKPOINT`. Allows PITR.
- __BULK LOGGED__: Used for bulk loading. Minimal logging. Best to do a full backup afterwards and after returning to __FULL__ recovery mode.

```sql
ALTER DATABASE db SET RECOVERY SIMPLE|FULL|BULK_LOGGED;
```

Full backup in any recovery model does:

- `CHECKPOINT`
- _data read phase_: every page is backed up
- _log read phase_: enough log for a consistent recovery
- RPO is at end of backup

Differential backup:

- Only in __FULL__ or __BULK_LOGGED__
- Not __SIMPLE__
- __FULL__ Only transaction logs
- __BULK_LOGGED__ Transaction logs plus modified pages that include minimally logged transactions
- Backup means VLFs are truncated until first active VLF is found
- Allow PITR
- Least resource intensive

TAPE backup deprecated

Backup device

- physical file on disk
- tape
- Azure BLOB

Media

- maximum of 64 backup devices
- can be mirrored/stripped within a media set
- Media family
- maximum of 4 mirrors for a device
- media set must be of same type, __DISK__ or __TAPE__

Logical Backup Device `sp_adddumpdevice`

Media Set: Each media family has:

- family sequence number
- physical sequence number

Backup Set - append/overwrite media

## Backup Strategies

- __FULL DATABASE__: Master, MBSDB. RPO is time of last backup
- __FULL__ plus __TRANSACTION LOG__ backup: RPO is frequency of transaction log backup. RTO determines frequency of FULL backup.
- __FULL__, __DIFFERENTIAL__, __TRANSACTION LOG__ backup: Differential is cumulative
- __FILEGROUP__ Backup
  - need only restore corrupt filegroup
  - Backup filegroup instead of files as tables are stored across multiple files in filegroups
- _Partial Backup_ - only read/write filegroup not read-only filegroup

Copy only backup is not entered into restore sequence. Does not reset for differential backup. No copy - only differential backup.

Can do copy-only transaction logs backup:

- log no truncated
- does not affect log archive point

'Perform Checksum Before Writing to Media' option chosen when doing backup more often than `DBCC CHECK DATABASE`.

```sql
BACKUP DATABASE db
  TO DISK='fn'
  WITH
    RETAINDAYS=90,
    FORMAT,
    INIT,
    MEDIANAME='...',
    NAME='...',
    COMPRESSION;

WITH DIFFERENTIAL ...

BACKUP LOG db
  TO DISK='fn'
  WITH
    RETAINDAYS=90,
    NOINIT,
    MEDIANAME='...',
    NAME='...',
    COMPRESSION;

/* INIT overwrites existing backup file */
/* FORMAT overwrites media headers */

BACKUP DATABASE db
  FILEGROUP='fg' ...
```

## Restoring a Database

`RESTORE WITH VERIFY ONLY`

- backup set is complex
- all backup device readable
- `CHECKSUM` valid
- page headers verified
- enough space for restore

Restore with restricted access:

- administrators
- `db_creator`
- `db_owner`

- `RECOVERY` - database online after restore completes
- `NORECOVERY` - database left in restoring state
- `STANDBY`
  - database online but read-only
  - failover to secondary server

`WITH PARTIAL` allows apply of additional backup even using `RECOVERY`. `PIECEMEAL` recovery. Tail log backup.

PITR:

- `sys.fn_dump_dblogs()`
- `MSDB.dbo.suspect_pages`

```sql
RESTORE DATABASE db
  PAGE='n:m'
  FROM DISK=N'...'
  WITH
    FILE=1,
    NORECOVERY,
    STATS=5;
BACKUP LOG db;
RESTORE LOG db;
```

## Piecemeal Restores

Use filegroup to backup and restore.
