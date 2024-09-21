---
layout: default
title: '05. Installation on Heterogeneous Operating Systems'
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
RECONFIGURE [WOITH OVERRIDE]
exec sp_configure 'show advanced options',1

SELECT * FROM sys.configurations
    WHERE is_dynamic = 1 /* needs reconfiguration */
    WHERE is_dynamic = 0 /* needs restart */
```

## Processor Affinity


