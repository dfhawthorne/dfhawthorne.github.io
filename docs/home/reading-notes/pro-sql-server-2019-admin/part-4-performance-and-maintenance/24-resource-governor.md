---
layout: default
title: '24. Resource Governor'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/24-resource-governor.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part IV. Performance and Maintenance'
  url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance
---

- Resource Pool
  - internal pool - instance
  - default pool
  - default external pool MLS
- Workload Group
- Classifier Function with parameters
  - username
  - role membership
  - application name
  - login property
  - connection property
  - time
  - etc.

- Max 64 resource pools per instance
- Max memory is a hard limit
- Max CPU is a soft limit, can be a hard limit

```sql
CREATE RESOURCE POOL <pool>
  CAP_CPU_PERCENT x /* hard limit */
  MAX_CPU_PERCENT y /* soft limit */
```

IOPS only managed if MAX set:

- only affects
- writes are done by instance
- not size of IOPS

```sql
CREATE EXTERNAL RESOURCE POOL ...;

CREATE RESOURCE POOL <app_pool> WITH (...);

ALTER RESOURCE GOVERNOR RECONFIGURE;
```

Memory grant % 0 =\> blocks SORT or HASH JOIN

Error 8657, DOP = 1 and not enough RAM

```sql
CREATE WORKLOAD GROUP <grp>
  WITH (...)
  USING <app_pool>;
ALTER RESOURCE GOVERNOR RECONFIGURE;
```

One classifier function per instance - returns `SYSNAME`. Must reside in Master database:

```sql
USE MASTER;
CREATE FUNCTION dbo.classifer
  RETURNS SYSNAME
  WITH SCHEMA BINDING
  AS BEGIN
    USER_NAME()
    HOST_NAME()
    ...

ALTER RESOURCE GOVERNOR
  WITH (CLASSIFIER_FUNCTION=dbo.classifier);
ALTER RESOURCE GOVERNOR RECONFIGURE;

EXECUTE AS LOGIN='...';

REVERT;
```

## Performance

```text
MSQSQL$[INSTANCE,NAME]
  Resource Pool Stats
  Workload Group Stats

sys.dm_resource_governor_resource_pools
sys.dm_resource_governor_workload_groups
```

