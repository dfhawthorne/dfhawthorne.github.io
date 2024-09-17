---
layout: default
title: '02. GUI Installation'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/02-gui-installation.html
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

Failover cluster - 2 to 64 nodes

Maintenance tab

- edition upgrade
- repair corrupt instance
- remove node from cluster

If the instance will not start, use CLI:

```bash
setup.exe ACTION=REBUILDDATABASE
```

Advanced tab: install based on a configuration file

Can create cluster configuration file. Use _Advanced Cluster Preparation_ on _Advanced_ tab.

After running the _Advanced Cluster Preparation Wizard_ on every possible node, run the _Advanced Cluster Completion Wizard_ on any node. Needs to be done once.

`SYSPREP` allows deployable vanilla images with SQL/Server installed. 2019+ Needs _Image Completion_ of a _Prepared Stand Alone Instance_ of SQL/Server option.

Slipstream is now deprecated in 2019. (allows insatllation of patches at the same time as binary installation)

15 is edition (2019) of SQL/Server

Max length of instance name is 16. (MSSQLSERVER is default) Up to 50 standalone instance on a single server.

Virtual sccounts - local accounts based on computer name.

__MSA__ (_Managed Service Accounts_) (AD)

Both can only be used on a single server.

Collation

- accent insensitivity
- Kana insensitivity. Hiragana = katakana
- case insensitivity

Windows authentication (best). Mixed mode is legacy.

Need at least one instance administrator. Ideally should be a Windows group to which all DBAs belong.

`FILESTREAM` and _File Table_ are covered in Ch 8.

