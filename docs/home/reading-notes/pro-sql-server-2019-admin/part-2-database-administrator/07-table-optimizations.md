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
