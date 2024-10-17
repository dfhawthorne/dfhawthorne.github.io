---
layout: default
title: '21. Distributed Replay'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/21-distributed-replay.html
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

- Controller - orchestrate clients
- Clients max 16
- Target only 1

`DReplay-Controller.config`

- _Admin Tool_
  - preprocess trace files
  - replay trace files
- `DReply.exe` `[preprocess|replay]` `<config>`
- RML = _Replay Markup Language`
- Capture events -\> XEL -\> `readtrace.exe` -\> trace
- 2 modes
  - stress - fires events as fast as possible
  - syncronisation - events in order
