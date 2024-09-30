---
layout: default
title: '08. Indexes and Statistics'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-2-database-administrator/08-indexes-and-statistics.html
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

"[SQL Server Advanced Data Types: JSON, XML, and Beyond](https://www.google.com.au/books/edition/SQL_Server_Advanced_Data_Types/l61qDwAAQBAJ)"

Clustered idex = IOT

Heap:

- IAM Indexed Allocation Map
- RID row-id (`FileID:PageID:Slot Number`)

Non-unique Clustered index requires an uniquifier.

By default, creating PK creates a clustered index unless one already exists.

GUID is 16 bytes. Every non-clustered index has to store GUID if PK. GUID is random. Overridden with `NEWSEQUENTIALID()` which is monotonically increasing - can start at a lower value after a restart.

Narrow PK though `IDENTITY` in order to reduce size of secondary indexes.

- 2004+ `CREATE TABLE PK INDEX`
- 2019+ `OPTIMIZE_FOR_SEQUENTIAL_KEY` to reduce last page insert contention

## Nonclustered Indexes

Covering indexes - only index columns are needed by query.

Key lookup:

- clustered index key
- RID

Index tipping ppoint 0.5% - 2%

## Covering Indexes

Instead of wide indexes, use included columns. These are only stored at the lead level.

Unique, noclustered index are narrowere than non-unique ones.

## Filtered Indexes

Built on a subset of data in the table. Filters: `NOT NULL`, `NULL`, `=`, `<>`, `>`, `<`, `<=`, `=>`, `IN`, `AND`, `OR`, simple predicate.

Not allowed: comparisons between columns, date functions, `CASE`, `BETWEEN`, `NOT IN`.

## Columnstore Indexes

Rowgroup 102,400 and 1,048,576 rows. Each column in a rowgroup in compressed using VeriPaq technology - column segment.

Batch execution mode - process 1,000 rows at a time - optimal for DW.

## Clustered Columstore Indexes

Whole table is trored in Columnstore format.

Deltastore: row storage (temp) for new rows to reduce fragmentation and to improve DML performance.

When deltastore becomes big enough a background process, called tuple, compresesses the deltastore into column segments within rowgroups.

Logical deletion for deletes and updates. Remains until next index rebuild. Identified through a B-tree:

```sql
CREATE CLUSTERED COLUMNSTORE INDEX
```

No need for key as all columns are added. Is the only index on the table. No PK, FK, or UK constraints. Not all column types are supported.

## Non-Clustered Columnstore Indexes

Not updatable. R/O. Drop/disable IDX, do DML, Create/Enable or use partition switching.

Can use other indexes.

## In-Memory Indexes

Must have at least one (max 8) for in-memory tables. Cover all columns.

Create through `CREATE TABLE`. `CREATE INDEX` is not allowed for in-memory. Indexes for in-memory are in memory only, and are recreated on restart.

## Nonclustered In-memory Hash Indexes

Large number duplicates require a large number buckets. Approximately 20-100 times number distinct keys instead of twice for unique index.

Different versions of rows exists in a hash bucket for non-unique, but only row version for an unique index.

> The amount of memory used by a nonclustered hash index always remains static, since the number of buckets does not change.

## Maintaining Indexes

Missing indexes - estimated query plan.

```text
sys.dm_db_missing_index_details
sys.dm_db_missing_index_groups
sys.dm_db_mising_index_group_stats
```

Index fragmentation:

- internal - pages with high free space
- external - pagaes out of order on disk

`FILLFACTOR` space for one row. `sys.dm_db_index_physical_stats`

`ONLINE` rebuild will fail if `ALLOW_PAGE_LOCKS` is off.

`MAXDOP=1` can reduce some residual fragmentation:

```sql
ALTER INDEX idx ON t REBUILD WITH (MAXDOP=1);
```

2019+ Resumable index operations:

- can pause, then resume
- reduces log usage
- no long running transactions
- degrades write performance during pause

```sql
WITH (MAXDOP=1,ONLINE=ON,RESUMABLE=ON)
ALTER INDEX idx ON t PAUSE
                     RESUME
                     ABORT
ALTER DATABASE SCOPED CONFIGURATION SET
```

## Statistics

`AUTO_CREATE_STATISTICS` - not for multi-column or filtered

Statistics always collected on index creation.

`AUTO_UPDATE_STATISTICS` process synchronisation and blocking

```text
AUTO_UPDATE_STATS_ASYNC
AUTO_CREATE_STATISTICS ON(INCREMENTAL=ON)
AUTO_UPDATE_STATISTICS ON WITH NO_WAIT
AUTO_UPDATE_STATS_ASYNC WITH NO_WAIT
```

Filtered statistics `WHERE`

Incremental statistics per partition not allowed in certain situations.

## Managing Statistics

`CREATE STATISTICS` filtered statistics require `WHERE`

```sql
CREATE STATISTICS sn ON t(...)
  FULLSCAN /* 100% */
  SAMPLE n /* n=0 means no collection */
  NORECOMPUTE
  INCREMENTAL;
UPDATE STATISTICS sn|t;
  RESAMPLE
  ON PARTITIONS ...
  ALL|COLUMN|INDEX
EXEC sp_updatestats 'RESAMPLE'; /* for database */
```

2019+

- `WAIT_ON_SYNC_STATISTICS_REFRESH`
- `SELECT (STATMAN)` indicates `SELECT` is waiting for statistics collection to complete
