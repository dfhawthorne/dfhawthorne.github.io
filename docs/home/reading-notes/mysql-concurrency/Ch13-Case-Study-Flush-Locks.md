---
layout: default
title: 'Ch 13: Case Study: Flush Locks'
base-url: home/reading-notes/mysql-concurrency/Ch13-Case-Study-Flush-Locks.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> The main symptom of a flush lock issue is that the database comes to a grinding halt where all new queries using some or all tables end up waiting for the flush lock.

## The Cause

> When a connection requests a table to be flushed, it requires all references to the table to be closed which means no active queries can be using the table.

## The Investigation

`state` in `sys.session` will show waiting reason. N/A in performance views.

Find waiting session, then look for queries that have been running longer.

Low level TDC lock can persist after `FLUSH TABLE` session has been killed. Now the waiting session is that was blocked by original `FLUSH TABLE` statement.

## The Solution

```sql
EXPLAIN FOR CONNECTION <process list>
```

Whether to kill the long running query that blocked the `FLUSH TABLE` statement depends on the amount of work done. See `trx_rows_modified` of the `information_schema.INNODB_TRX` view.

Rollback of DML can take much longer than the original application of changes.

## The Prevention

> The flush lock contention happens because of the combination of a long running query and a `FLUSH TABLE` statement.
>
> __Tip__ To avoid long-running `SELECT` queries, you can configure the max_execution_time option or set the `MAX_EXECUTION_TIME(N)` optimizer hint. This will make the `SELECT` statement time out after the specified period and help prevent issues like flush lock waits.

Or schedule long running queries.

MySQL Enterprise Backup (MEB) avoids `FLUSH TABLE` when taking a backup. 8.0.16+

Do backup while system is read/only.
