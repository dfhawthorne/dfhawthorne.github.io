---
layout: default
title: 'Ch 14: Case Study: Metadata and Schema Locks'
base-url: home/reading-notes/mysql-concurrency/Ch14-Case-Study-Metadata-and-Schema-Locks.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

MySQL 8+ Instrumentation enabled by default for metadata locks.

## The Symptoms

Similar to `FLUSH TABLE` scenario.

DDL "Waiting for table metadata lock."

`ER_LOCK_WAIT_TIMEOUT` 1205 `lock_wait_timeout`

## The Cause

> In a typical situation, there will be a long-running query or transaction, a DDL statement waiting for the metadata lock, and possibly queries pilling up.

Also explicit locks:

- `LOCK TABLE`
- `FLUSH TABLES WITH READ LOCK`

## The Investigation

wait/lock/metadata/mdl: Performance schema instrument enabled. Default for MySQL 8+

`schema_table_lock_waits`

> __Note__: that what InnoDB calls the MySQL thread id (the `trx_mysql_thread_id` column) is actually the connection id.

- `events_transactions_current`
- `session_connect-info`

> Not all clients and connections submit attributes or they may be disabled so this information is not always available.

## The Solution

If there is a large amount of UNDO, kill DDL first then idle transactions to allow blocked queries to proceed while the rollback is processing. Then retry DDL once rollback is done.

## The Prevention

Avoid DDL during high activity. Set `lock_wait_timeout` low.
