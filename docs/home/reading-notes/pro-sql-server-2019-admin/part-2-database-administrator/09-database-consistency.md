---
layout: default
title: '09. Database Consistency'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-2-database-administrator/09-database-consistency.html
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

- 605 error: (sev12) => dirty read
  - Read uncommitted
  - `NOLOCK`
  - (sev21) => possible damaged page `DBCC CHECKDB`
- 823 error: I/O error (physical) `DBCC CHECKDB`
- 824 error: logical inconsistency
- 5180 error: invalid file ID
- 7105 error: non-existent LOB - could result from a dirty read

Page verify (DB level)

- `CHECKSUM` \<\= default
- `TORN_PAGE_DETECTIOn` (deprecated)
- `NONE`

```sql
ALTER DATABASE db SET PAGE_VERIFY CHECKSUM WITH NO_WAIT;
```

`dbo.suspect_pages`

```sql
ALTER DATABASE db SET SINGLE_USER WITH NO_WAIT;
DBCC WRITEPAGE
ALTER DATABASE db SET MULTI_USER WITH NO_WAIT;
```

In-memory cannot be repaired through `DBCC CHECKDB`. Need to check backup of in-memory table for errors.

Corrupt Master - rebuild sys database

```bash
setup.exe /ACTION Rebuilddatabase /INSTANCENAME inst /Q
```

Restore MDB from backup. Reattach user database.

Corrupt Res DB or binary:

- Repair utility on SQL install media
- Repair from Maintenance tab of SQL/Server Installation Centre

```bash
setup.exe /ACTION Repair /INSTANCENAME inst
DBCC CHECKDB WITH ...
```

## Fixing Errors

- `REPAIR_BUILD` preferred
- `REPAIR_ALLOW_DATA_LOSS` if no backup
- none => report minimum level of repair

Repair requires single user mode:

```sql
ALTER DATABASE db SET SINGLE_USER;
DBCC CHECKDB(db,opt)
ALTER DATABASE db SET MULTI_USER;
```

Emergency mode is last resort. Inaccessible pages => non errors in this mode:

```sql
ALTER DATABASE db SET EMERGENCY;
ALTER DATABASE db SET SINGLE_USER;
DBCC CHECKDB(db,opt)
ALTER DATABASE db SET MULTI_USER;
DBCC CHECKCATALOG
DBCC CHECKALLOC
DBCC CHECKTABLE
DBCC CHECKFILEGROUP
DBCC CHECKIDENT
DBCC CHECKCONSTRAINTS /* run after CHECKDB */
```

`DBCC CHECKDB` with `PHYSICAL_ONLY` only detects physical I/O errors

Full backup everynight plus `PAGE_VERIFY CHECKSUM`. Add `WITH CHECKSUM` to full backup. Then use `DBCC CHECKALLOC` instead of `DBCC CHECKDB PHYSICAL_ONLY`. Still need weekly `CHECKDB` to detect logical and in-memory errors.

With multiple filegroup, split workload by running `CHECKFILEGROUP` on subsets every night. Still need weekly `CHECKDB`.
