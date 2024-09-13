---
layout: default
title: 'Ch 16: Case Study: Deadlocks'
base-url: home/reading-notes/mysql-concurrency/Ch16-Case-Study-Deadlocks.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---


## The Symptoms

`ER_LOCK_DEADLOCK` `lock_deadlocks++`

```text
sys.metrics
  variable_name = 'lock_deadlocks'
event_errors_summary_global_by_error
  error_name = 'ER_LOCK_DEADLOCK'
  error_number = 1205
```

```sql
SHOW ENGINE INNODB STATE LATEST DETECTED DEADLOCK
```

## The Cause

> Deadlocks are caused by locks being obtained in different orders for two or more transactions.

## The Investigation

Enable `innodb_print_all_deadlocks` (OFF by default). See error log for details. Does show which transaction was rolled back.

## The Solution

Automatically resolved.

## The Prevention

- Smaller transaction
- `READ COMMITTED`
- Shorted transaction
- Pessimistic locking
