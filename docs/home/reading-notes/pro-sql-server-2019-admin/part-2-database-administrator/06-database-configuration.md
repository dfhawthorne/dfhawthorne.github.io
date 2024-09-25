---
layout: default
title: '06. Database Configuration'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-2-database-administrator/06-database-configuration.md
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part II. Database Administrator'
  url: home/reading-notes/pro-sql-server-2019-admin/part-2-database-administrator
---

Database:

- Transaction Log
- Primary File Group:
  - primary file
  - secondary file
- File group
  - secondary file

First file = primary (`*.mdf`) in primary file group. All other files are secondary (`*.mdf`)

Tables and indexes are stored in file groups. File group can be considered to equivalent to a tablespace.

| File ID | Description |
| ---: | --- |
| 1 | Primary file |
| 2 | Transaction log |

8K page has 96 bytes of overhead. 8 pages comprise an extent.

### Filestream Filegroup

Unstructured data (BLOBs) stored in operating system files. There is a performance advantage for BLOBs larger than 1 MB.

Need memory allocated to file cache rather than buffer cache.

Filegroups point to directories rather than files.

Location = container. Enable `FILESTREAM`.

```sql
ALTER DATABASE db
    ADD FILEGROUP fg
    CONTAINS FILESTREAM;
```

GUID not suitable for PK

`ROWGUIDCOL` is needed for LOBs in __FILESTREAM__.

File table builds on __FILESTREAM__. Is this the same thing as external tables?

## Memory-Optimized Filegroups

Only one (1) memory-optimized filegroups per database. Available 2014+ Consists of:

- Data file (updates and inserts)
- Delete file (updates and deletes)

```sql
ALTER DATABASE db
    ADD FILEGROUP fg
    CONTAINS MEMORY_OPTIMIZED_DATA;
```

## File Group Performance

Fast Track Data Warehouse Reference Architecture

Placing partitions in separate filegroup prevents partitioning functions (e.g. `SWITCH`).

## Backup

DB, FG, File - piecemeal restore

## Storage-Tiering Strategies

AO (Adaptive Optimization) is problematic in SQL/Server

For memory-optimized, place 2 containers in each filegroup which maps to a spindle.

## File and File Group Maintenance

```sql
ALTER DATABASE db
    ADD FILE (
        N'm',
        FILENAME=N'X:\..',
        SIZE=xKB,
        FILEGROWTH=yKB
    )
    TO FILEGROUP fg;
```

Beware of proportional filling.

```sql
DBCC SHRINKFILE
DBCC EMPTYFILE
```

- `TRUNCATEONLY` shrinks to end of highest allocated extent.
- `NOTRUNCATE` shuffles extent from high to low.

```sql
USE db;
DBCC SHRINKFILE(N'fn',0,TRUNCATEONLY)
DBCC SHRINKDATABASE(N'db')
```

Shrinking is a rare event. `AUTOSHRINK` is a bad idea. DB shrink is slow as it is single-threaded.

__NOTE:__ Never use `NOTRUNCATE` as this causes fragmentation issues.

## Database Scoped Configuration

2016+: `T1117` and `T1118` have no effect.

| Parameter | Event |
| --- | --- |
| `AUTOGROW_ALL_FILES` | `T1117` |
| `MIXED_PAGE_ALLOCATION` `OFF` | `T1118` |

## Log Maintenance

VLF (Virtual Log File) cannot be reused. Causes log file to grow.

9002 error if log file cannot grow

Increment:

- less than 64MB, then 4 VLF
- greater than 1GB, then 16 VLF
- else 8 VLF

## Recovery Model

| Recovery Model | Description |
| --- | --- |
| SIMPLE | No backup of log. Auto-truncate log. No HADR. RPO is last full or increment backup. |
| FULL | Log must be backed up. Log is truncated during backup. Allows PITR. |
| BULK LOGGED | FULL is suspended while doing bulk load. No PITR |

Log File Count greater than 1. No valid reason unless there are space issues.

Shrinking log is not needed unless bulk load or ETL was done:

- take log file backup
- shrink in single user mode

## Log Fragmentation

Grow log file in 8GB chunks. Large VLF take a long time to clear thereby slowing performance. Too small implies large number of VLF which slows down transactions.

```sql
DBCC LOGINFO undo
SELECT log_reuse_wait_desc
    FROM sys.databases
    WHERE name = 'db';
```

Reason applies at time log attempts to recycle

All backup sequences must begin with full backup.

Change VLF by shrinking then expanding in larger increment.

## Summary

> Filegroups are logical containers for data files. Special filegroups also exist for `FILESTREAM`/`FileTable` data and for memory-optimized data. When tables and indexes are created, they are created on a filesgroup as opposed to a file, and the data in the object is distinguished evenly across the files within that filegroup.
