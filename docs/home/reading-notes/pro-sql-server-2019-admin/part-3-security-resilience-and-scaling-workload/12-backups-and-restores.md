---
layout: default
title: '12. Backups and Restores'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/12-backups-and-restores.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part III. Security Resilience and Scaling Workload'
  url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload
---

- __SIMPLE__: Low overhead, RPO is last backup. Log truncation is done at `CHECKPOINT`.
- __FULL__: Log truncated after log backup and `CHECKPOINT`. Allows PITR.
- __BULK LOGGED__: Used for bulk loading. Minimal logging. Best to do a full backup afterwards and after returning to __FULL__ recovery mode.

```sql
ALTER DATABASE db SET RECOVERY SIMPLE|FULL|BULK_LOGGED;
```

Full backup in any recovery model does:

- `CHECKPOINT`
- _data read phase_: every page is backed up
- _log read phase_: enough log for a consistent recovery
- RPO is at end of backup
