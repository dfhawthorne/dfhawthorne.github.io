---
layout: default
title: '17. SQL Server Metadata'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/17-sql-server-metadata.html
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

Catalogue views are in SYS schema.

`INFORMATION_SCHEMA` based on ISO standards.

DMV - Dynamic Management Views and functions

| Prefix | Description |
| --- | --- |
| `dm_` | Dynamic management |
| `dm_os_` | Operating system |
| `dm_db_` | Database |
| `dm_io_` | I/O |
| `dm_exec_` | Execution |

`DB_ID()`, `OBJECT_ID()`, `DATALENGTH()`

## Server-Level and Instance-Level Metadata

```text
sys.dm_server_registry
  registry_key
  value_name
  value_data
```

Can find find listener port from registry also startup parameters, `SQLArg%`.

```text
sys.dm_server_sources
sys.dm_os_buffer_descriptors
sys.dm_db_file_space_usage
sys.dm_io_virtual_file_stats
sys.master_files
xp_fixeddrives
```

Use of `xp_cmdshell` is against security best practice.

## Metadata for Troubleshooting and Performance Tuning

`sys.dm_os_performance_counters`

- Running
- Runnable signal wait
- Suspended
  - Resource wait
  - Queue wait

`sys.dm_os_wait_stats`

## Database Metadata

- \< 2019 `DBCC PAGE`
- 2019+ `sys.dm_db_page_info`

## Metadata-Driven Automation

- Rolling DB snapshots
- Rebuild fragmented indexes
