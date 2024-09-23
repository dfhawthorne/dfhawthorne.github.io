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
- title: 'Part I. Installation and Configuration'
  url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration.html
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
