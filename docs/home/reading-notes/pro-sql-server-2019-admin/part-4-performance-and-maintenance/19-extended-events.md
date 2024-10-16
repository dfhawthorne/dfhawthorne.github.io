---
layout: default
title: '19. Extended Events'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/19-extended-events.html
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

> The predecessor to Extended Events was SQL Trace, and its GUI, called Profiler. This is now deprecated for use with the Database Engine, and it is recommended that you only use it for tracing Analysis Service activity.

## Extended Events Concepts

- Packages
  - Package0
  - SqlServer
  - SqlOS
  - SecAudit

> An event is an occurrence of interest that you can trace

- Channels (H/L category)
  - Admin
  - Operational
  - Analytic (high volume)
  - Debug

KW aka category

> A target is a consumer of events

- Channels (Cont.)
  - event counter
  - event file
  - ETW
  - Histogram
  - Ring Buffer
- Actions gather extra info
- Predicate - filter conditions
- Types (`sys.dm_xe_objects`)
- Maps - internal ID to human readable (`sys.dm_xe_map_values`)

> A session is essentially a trace
>
> When a session starts, events are written to memory buffers and have predicates applied before they are sent to the target

`NO_EVENT_LOSS` option for `EVENT_RETENTION_MODE` causes performance issues!

> Data viewer does not support the ring buffer or ETW target types

`sys.fn_xe_file_target_read_file`

> Perfmon counters are in the Analytic channel but have no category
>
> The SQL Server service account must be in the Performance Log Users group, or an error is thrown.
>
> Events are points of interest that are captured in a trace, whereas actions provide extended information, in addition to the event columns. Predicates allow you to filter events in order to provide a more targeted trace, and targets define how the data is stored. A session is the trace object itself and can be configured to include multiple events, actions, predicates, and targets.
