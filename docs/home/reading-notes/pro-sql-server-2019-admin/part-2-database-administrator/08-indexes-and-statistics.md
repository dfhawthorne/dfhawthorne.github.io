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
