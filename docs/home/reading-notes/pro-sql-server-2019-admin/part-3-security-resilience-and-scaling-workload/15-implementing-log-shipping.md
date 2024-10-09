---
layout: default
title: '15. Implementing Log Shipping'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/15-implementing-log-shipping.html
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

FULL recovery model

Log monitor server plus backup share

```text
sp_add_log_shipping_primary_database
sp_add_schedule
sp_attach_schedule
sp_update_job

sp_add_log_shipping_primary_secondary

sp_add_log_shipping_secondary_primary
sp_add_schedule --copy
sp_attach_schedule
sp_add_schedule --restore
sp_attach_schedule
sp_update_job /* to enable both copy and restore jobs */
sp_add_log_shipping_secondary_database
sp_process log shipping monitor secondary
```

Failover:

- tail end log backup
  - `no_truncate`
  - `NORECOVERY`
- apply `NORECOVERY` until tail end log which is applied with `RECOVERY`

Switch roles

- disable backup, copy, and restore jobs
- rebuild jobs as above
- synchronisation "No, The Secondary Database is Initialized"

```text
sp_change_log_shipping_secondary_database
sp_change_log_shipping_primary_database
sp_help_log_shipping_monitor
```

Log __STANDBY__ uncommitted transaction on Transaction Undo File

- Error 14420 backup threshold exceeded
- Error 14421 restore threshold exceeded
