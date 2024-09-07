---
layout: default
title: 'Ch 09: Reducing Lock Issues'
base-url: home/reading-notes/mysql-concurrency/Ch09-Reducing-Lock-Issues.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> An important strategy to resolve lock issues is to keep your transactions small and to avoid delays that keep the transaction open for longer than necessary.
>
> The duration of the transaction is also important. One common problem is connections using autocommit = 0. This starts a new transaction every time a query (including SELECT) is executed without an active transaction, and the transaction is not completed until an explicit COMMIT or ROLLBACK is executed, a DDL statement is executed, or the connection is closed.
>
> Another pitfall is to start a transaction and perform slow operations in the application while the transaction is active. This can be data that is sent back to the user, interactive prompts, or file I/O. Make sure that you do these kinds of slow operations when you do not have an active transaction open in MySQL.

## Indexes

> Indexes reduce the amount of work performed to access a given row. That way indexes are a great tool to reduce locking as only records accessed while executing the query will be locked.

- FTS locks all rows
- IX locks matching rows

With index, locks are:

| Object | Lock |
| --- | --- |
| Table | `IS` |
| Name Record | `S` |
| Primary Record | `S,REC_NOT_GAP` |
| Name Record | `S,GAP` |

> On the flip side, more indexes provide more ways to access the same rows which potentially can increase the number of deadlocks .

## Record Access Order

Access records in same order across multiple transactions especially join order.

## Transaction Isolation Levels

Repeatable Read and serializable have more locks than Read Committed.

> The READ COMMITTED transaction isolation level can help on locking issues in two ways. Far less gap locks are taken, and rows that are accessed during a DML statement but not modified have their locks released again after the statement has completed. For REPEATABLE READ and SERIALIZABLE, locks are only released at the end of the transaction.

This is not strictly true:

> If you are migrating an application from Oracle DB, you are already using READ COMMITTED, and you can also use it in MySQL.

## Resource Partitioning

`innodb_adpative_hash_index_part`

- 8 default
- adaptive hash index

`innodb_buffer_pool_instances`

- = 1 if less than 1 GB
- = 8 else (default)
- Less than or equal 64

`table_open_cache_instnces` = 16 (default)

> In general, you should not have the number of partitions larger than the number of CPU cores.

## Disabling the INNODB Adaptive Hash Index

> If InnoDB detects that you are using a secondary index frequently and adaptive hash indexes are enabled, it will build a hash index on the fly of the most frequently used values.
>
> The larger the part of the working data set that does not fit into the buffer pool, the more changes you have to the secondary indexes, and the less the secondary indexes are used for filtering, the more likely you will benefit from disabling the adaptive hash index.
>
> ...the adaptive hash index is a problem typically manifest themselves through a high number of waits on mutexes and rw-lock semaphores in the `btr0sea.cc` file which is where the adaptive hash index search is implemented.

## Reducing Priority of Metadata Write Locks

Write priority \> read priority

FK problems

`max_write_lock_count` when exceeded, reads will have a higher priority:

> You can do that with the `max_write_lock_count` option which takes a value between 1 and the maximum supported integer for your system. The default is the maximum supported value. Every time `max_write_lock_count` locks have been granted, MySQL will give priority to some read locks. This helps ensuring that read lock requests are not starved.

## Preemptive Locking

```sql
SELECT FOR UPDATE|SHARE
```

Can reduce deadlocks, but locks are held for longer.
