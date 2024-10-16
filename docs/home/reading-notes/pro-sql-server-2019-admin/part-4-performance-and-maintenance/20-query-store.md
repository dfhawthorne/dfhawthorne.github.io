---
layout: default
title: '20. Query Store'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/20-query-store.html
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

2016+: Query history, plans, statistics at DB level

```sql
ALTER DATABASE db SET QUERY_STORE=ON;
```

```text
QUERY_CAPTURE_POLICY
STALE_CAPTURE_THRESHOLD
EXECUTION_COUNT
TOTAL_COMPILE_CPU_TIME_MS
TOTAL_EXECUTION_CPU_TIME_MS

query_store_plan
query_store_query
query_store_wait_stats
query_store_query_stats
query_store_runtime_stats

sp_query_store_flush_db
sp_query_store_force_plan
sp_query_store_unforce_plan
sp_query_store_reset_exec_stats
sp_query_store_remove_plan
sp_query_store_remove_query
```

2019+ more granular control over capture
