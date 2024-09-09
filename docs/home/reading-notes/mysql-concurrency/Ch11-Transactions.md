---
layout: default
title: 'Ch 11: Transactions'
base-url: home/reading-notes/mysql-concurrency/Ch11-Tranactions.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> InnoDB does not support deferred constraints but does support disabling foreign key checks by explicitly disabling the `foreign_key_checks` variable which can be changed both at the global and session scope.
>
> Unique key constraint checks cannot be disabled for InnoDB as the `unique_checks` option only dictates that a check is not required;
> 
> The commits are only guaranteed to be durable if both `innodb_flush_log_at_trx_commit` and `sync_binlog` are set to 1 (the default).

## Impact of Transactions

Main resources are locks and undo logs.

> For multi-statement transactions, you can specify explicitly that it is a read-only transaction, when you start it: `START TRANSACTION READ ONLY;`

Read only transactions have a lower overhead.

> Thus, the more locks you hold and the longer they are held, the less memory is available for caching data and indexes.

## Locks

The default for RR is that all locks are kept until end of transaction.

> ...a transaction that has made no changes also can make undo information from other transactions stay around. This happens when the transaction requires a read view (a consistent snapshot), which is the case for the duration of the transaction when using the REPEATABLE READ transaction isolation level.
> 
> Long-running transactions with a read view are the most common reason for ending up with huge undo logs,...
> 
> __Tip__ The `READ COMMITTED` transaction isolation level is much less prone to large undo logs as the read views are only maintained for the duration of a statement.

With `READ COMMITTED`, some locks may be released early.

`ER_LOCK_TABLE_FULL`

> ...the more locks you hold and the longer they are held, the less memory is available for caching data and indexes.

A full lock table condition takes a while to clear as the offensive transaction is rolled back. Meanwhile, the database is effectively read-only.

There is a warning at 67% of the buffer pool.

Shared metadata locks are held to the end of transaction (EOT).

## Undo Logs

RR requires undo logs in order to get a consistent view of the data (read view).

Long running transactions with read view cause huge undo log files.

MySQL8+ undo log files are separate tablespace which be truncated.

Read Committed transactions only keep undo for the duration of the statement.

> The size of the active part of the undo log is measured in the history list length.

> __Note__: The issue with the history list length is one of the biggest issues creating backups of large databases using logical backup tools such as `mysqlpump` and `mysqldump` using a single transaction to get a consistent backup. The backup can cause the history list length to become very large if there are many transactions committed during the backup.
                
> Remember that for the D in ACID (durability) to be true for InnoDB, you need to keep the `innodb_flush_log_at_trx_commit` and `sync_binlog` settings at their default value of 1 so the changes made by a transaction are synced to disk as part of the commit.

INNODB ato purges UNDO logs

```text
innodb_purge_batch_size
    # pages purge (default 300)
innodb_purge_threads (4)
    Increase for large # tables change
    Decrease for small # tables change
innodb_max_purge_lag
    length > increases delay to transactions starting
    0 = no delay ever
innodb_max_purge_delay
    used for above
```

## Group Commit                

> Essentially, the group commit sacrifices a little latency for a higher throughput.

Durability requires:

- `innodb_flush_log_at_trx_commit=1`
- `sync_binlog=1`

Group commit batches commits.

`binlog_group_commit_sync_delay`: window in which to capture commits prior to flushing to disk.

`binlog_group_commit_sync_no_delay_count`: max # transactions before flushing to disk. 0 = unlimited (default)

Can improve performance on replicas.

