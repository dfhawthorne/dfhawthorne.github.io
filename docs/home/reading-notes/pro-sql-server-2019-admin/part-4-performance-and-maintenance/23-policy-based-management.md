---
layout: default
title: '23. Policy-Based Management'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/23-policy-based-management.html
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

- __Targets__ - entities managed
- __Facets__ - collection of properties (target)
- __Conditions__
- __Policies__ - bind conditions to targets

```sql
SELECT name FROM msdb.dbo.syspolicy_managements_facets
```

Evaluation Modes

- on demand
- on schedule
- on change: log only
- on change: prevent

Error 43053 sev 16

_CMS_ - central management server

Nested triggers need to be enabled on an instance

```sql
EXEC sp_configure 'nested triggers',1;
RECONFIGURE
```

Part of PBM, not T-SQL:

- `ExecuteSQL()`
- `ExecuteWql()` - security risk
- `sys.dm_server_services`
- `Win32-Service`

Powershell:

- Invoke - PolicyEvaluation
- 2000,2005 use XML for policy source
