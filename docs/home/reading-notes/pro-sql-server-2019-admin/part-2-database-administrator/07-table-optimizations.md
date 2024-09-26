---
layout: default
title: '07. Table Optimizations'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-2-database-administrator/07-table-optimizations.md
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

Partitioning key must be a subset of the clustering index key, if it exists.

Partitioning key can be on a computed value as long as it is persisted.

Partition Scheme maps partition to a filegroup. An extra filegroup is needed for new partition.

Index alignment:

1. same partition function and partition scheme
1. partition equality = data type, number of partitions, and boundary points.

Clustered index is always aligned because it shares physical storage with table.

Alignment assists in partition elimination.

```sql
CREATE PARTITION FUNCTION y AS
    RANGE LEFT FOR VALUES(x1,x2,x3,...);
CREATE PARTITION SCHEME s
    AS PARTITION y ALL TO (fg);
CREATE TABLE t (...) ON s(key);
ALTER TABLE TABLE t ADD CONSTRAINT
    pk PRIMARY KEY CLUSTERED (k1,k2,...)
    WITH (
        STATISTICS_NORECOMPUTE=OFF,
        IGNORE_DUP_KEY=OFF,
        ALLOW_ROW_LOCKS=ON,
        ALLOW_PAGE_LOCKS=ON
    )
    ON s(key);
```

Instead of creating a table on a filegroup, table is created on a partition scheme.

Partitioning an existing table:

- drop clustering index
- recreate cluster index on partition scheme

## Monitoring Partitioned Tables

`$PARTITION.PartFunc(part_key)` Can use with different partition function

Sliding windows:

- new partition added automatically
- oldest partition dropped automatically

- `SPLIT` adds new boundary point
- `MERGE` removes boundary point
- `SWITCH` moves partition into empty table or partition
  - metadata operation
  - does not physically move destination
  - all non-clustered index must be aligned with base table

`MERGE` and `SPLIT` can be used with different filegroup. This causes performance impact.

## Table Compression

Improves performance for I/O bound workload. Compression uses minimal data type needed to hold value. Single byte for Unicode. Row compression.

Page compression:

- row compression
- prefix compression  (longest value anchor)
- dictionary compression (duplicate values)

- `COLUMNSTORE` (is imcompatible with page compression) 2012+
- `COLUMNSTORE_ARCHIVE` 2014+ for infrequently accessed data

```sql
EXEC sp_estimate_data_compression_savings
ALTER TABLE t
    REBUILD WITH (
        DATA_COMPRESSION=<ROW|NONE>
    );
ALTER TABLE t
    REBUILD PARTITION p WITH ...
```

Table -> Storage -> Manage Compression

For heap tables, new pages are not auto-compressed. Needs regular manual rebuild.

- `SWITCH` both have same compression level
- `MERGE` set to destination compression level
- `SPLIT` inherit from parent

## Memory-Optimized Tables

- disk-based versions - unstructured in `FILESTREAM`
- memory optimized checkpoints happen more frequently
  - autocheckpoint after log grows by 512MB since last checkpoint
  - less data logged - only tables not indexes

In-memory OLTP reduces CPU overhead through natively compiled procedures.

- Increases memory pressure
- Designed for OLTP
- No latching for access
- Uses new optimistic concurrency

- `SCHEMA_AND_DATA` all logged plus data persisted
- `SCHEMA_ONLY` no logging or persistence

Needs memory-optimized filegroup. Must include an index:

- nonclustered hash index
- nonclustered index

#memory buckets is appox. equal to twice #distinct keys

Cannot aletr table or index

Performance test:

```sql
SET STATISTICS TIME ON
DBCC FREEPROCCACHE
DBCC DROPCLEANBUFFERS
```

DLL created for memory-optimized table

- recompiled everytime DB server restarts
- auto-deleted when table is dropped

## Natively Compiled Stored Procedures

```sql
BEGIN ATOMIC
```

Autocommit at end

```sql
WITH NATIVE_COMPILATION
    SCHEMA_BINDING /* prevents DDL on reference objects */
    EXECUTE AS ... /* DEFAULT of CALLER is not valid here */
```
