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

SSIS is incorporated into the DB engine. When SSIS (SQLServerInt.Serv) run, they run in a separate process and are not restricted by processor affinity.

Align processors on same NUMA node.

Do not use processor affinity with VM oversubscription because NUMA boundaries are not restricted.

For active/active failover, processor affinity should be so as to guarantee sonsistent performance in the event of a failover.

Processor affinity avoids overhead associated with moving threads between processors at the operating system level.

Afinity I/O mask:

- lazy writer
- usually used on 32 bit systems

Do align Affinity I/O Mask and processor mask onto the same core.

Bitmap in signed 32-bit integer or 64-bit.

```sql
EXEC sp_configure 'affinitt mask',15 RECONFIGURE
```

For 256 logical processors (max), use:

```sql
ALTER SERVER CONFIGURATION SET PROCESS AFFINITY CPU=4 TO 3
ALTER SERVER CONFIGURATION SET PROCESS AFFINITY NUMANODE=0,14
```

__MAXDOP__ will set the maximum number of cores that will be made available to each individual execution of a query.

`CXPACKET` want type

```text
MAXDOP = min(8, #cores, #cores in NUMA node)
0 = all visible cores
```
