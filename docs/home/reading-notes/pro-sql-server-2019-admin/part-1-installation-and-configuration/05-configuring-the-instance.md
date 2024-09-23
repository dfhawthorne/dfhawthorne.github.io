---
layout: default
title: '05. Configuring the Instance'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-1-installation-and-configuration/05-configuring-the-instance.html
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

`sp_configure`

- Name
- Minimum
- Maximum
- Configuration Value
- Run Value

If configuration value does not equal run value, either restart or reconfiguration is needed.

```sql
exec sp_configure $parm $val
RECONFIGURE [WITH OVERRIDE]
exec sp_configure 'show advanced options',1

SELECT * FROM sys.configurations
    WHERE is_dynamic = 1 /* needs reconfiguration */
    WHERE is_dynamic = 0 /* needs restart */
```

## Processor Affinity

SSIS is incorporated into the DB engine. When SSIS (SQLServerInt.Serv) run, they run in a separate process and are not restricted by processor affinity.

Align processors on same NUMA node.

Do not use processor affinity with VM oversubscription because NUMA boundaries are not restricted.

For active/active failover, processor affinity should be so as to guarantee sonsistent performance in the event of a failover.

Processor affinity avoids overhead associated with moving threads between processors at the operating system level.

Afinity I/O mask:

- lazy writer
- usually used on 32 bit systems

Do align Affinity I/O Mask and processor mask onto the same core.

Bitmap in signed 32-bit integer or 64-bit.

```sql
EXEC sp_configure 'affinity mask',15
RECONFIGURE
```

For 256 logical processors (max), use:

```sql
ALTER SERVER CONFIGURATION SET PROCESS AFFINITY CPU=4 TO 3
ALTER SERVER CONFIGURATION SET PROCESS AFFINITY NUMANODE=0,14
```

## MAXDOP

`MAXDOP` will set the maximum number of cores that will be made available to each individual execution of a query.

`CXPACKET` want type

```text
MAXDOP = min(8, #cores, #cores in NUMA node)
0 = all visible cores
```

```sql
EXEC sys.sp_configure 'max degree of parallelism',8
RECONFIGURE
```

`LMAXDOP` increases parallel plan threshold. Default is 5 seconds. This is ignored if `MAXDOP` = 1.

```sql
EXEC sys.sp_configure 'cost threshold for parallelim',10
RECONFIGURE
```

## Min and Max Server Memory

- Buffer cache
- Procedure cache (shared pool)
- Log cache
- Log pool (HA/DB, data distribution)
- CLR. .NET code within database

Usually MIN = MAX (avoids overhead of dynamically allocation memory)

Benefit with multiple instances

min (RAM - 2GB, (RAM / 8) * 7)

## Trace Flags

```sql
DBCC TRACEON(x,-1) /* Global */
DBCC TRACEON(x) /* Current process */
DBCC TRACESTATUS
DBCC TRACEOFF(x,-1) /* Global */
DBCC TRACEOFF(x) /* Current process */
```

These settings are transient - lost on restart. Persist through `-T` startup parm

- __T1117__ all files in a file group to grow at same rate - no longer used
- __T1118__ all extents to be uniform - no longer used
- __T3042__ stop autogrowth of backup file
- __T3226__ suppress successful backup messages in log (`sys.sp_readerrlog`)
- __T3625__ limit amount of metadata in error messages

## Ports

Named instance can use dynamic ports - no recommended because of difficulty with firewalls.

| Service | Port | Protocol |
| --- | ---: | --- |
| Browser | 1433 | TCP |
| Instance over TCP/IP | 1433 | TCP |
| Instance over Named Pipes | 445 | TCP |
| DAC (Dedicated Admin Console) | 1434 | TCP |
| Service Broker | 4022 | TCP |
| Always on Availability Group | 5022 | TCP |
| Merge replication with Web Sync | 21 |TCP |
| | 80 | TCP |
| | 137 | UDP |
| | 138 | UDP |
| | 139 | TCP |
| | 445 | TCP |
| T-SQL Debugger | 135 | TCP |

## System Databases

- `mssqlsystemresource` (Resource) store system objects
- `MSDB` (Metadata repository for features) `EXEC sys.sp_deletebackuphistory`
- `Master` (metadata for instance level objects)
- `Model` template for new database.  Recovery mode = Full => all new database configuration have the same model. `TempDB` is built off `Model`.
- `TempDB`workspace used by SQL Server when it needs to create a temporary object
  - temporary tables
  - table vatriables
  - sorting and spooling data
  - hashing data
  - online index operation
  - index operations
  - triggers
  - DBCC undo
  - DML output
  - Row versioning

```text
sys.dm_db_session_space_usage
sys.dm_db_task_space_usage
sys.dm_db_file_space_usage (Temp database data only available in TempDB context)
sys.dm_tran_version_store
sys.dm_tran_active_snapshot_database_transactions
```

One (1) `TempDB` file per core. Min 2, Max 8. More is needed if there is GAM/SGAM contention:

- `PATCHLATCH` waits against `TempDB`
- `PAGEIOLATCH` underlying storage is the issue

2019: Memory optimized `TempDB` Metadata cannot access mem-opt objects across multiple databases.

## Buffer Pool Extension

`WAL` Write ahead Logging

__Buffer Pool Extension__ designed for SSD.

- Secondary cache for clean pages only after eviction from RAM cache.
- Good for read-intensive
- Bad for write-intensive
- RAID10
- 4-8 times Max Server Memory

## Hybrid Buffer Pool

- `PMEM` persistent memory
- `SCM` storage class memory

On memory bus SSD. Direct access. Allocation Unit 2MB.

Transaction logs can be stored here.

Enlightment - memory mapped I/O only used for clean pages

Enable trace flag 809 (Windows) or 3979 (Linux).
