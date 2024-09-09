---
layout: default
title: 'Ch 12: Transaction Isolation Levels'
base-url: home/reading-notes/mysql-concurrency/Ch12-Tranactions-Isolation-Levels.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> The repeatable read transaction isolation level is the default.

## Serializable

> The SERIALIZABLE isolation level is the strictest available. Except for SELECT statements with autocommit enabled (and no explicit transaction has been started), all statements take locks.

```sql
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

> This transaction isolation level is not used very often, but it can be useful when investigating locking problems or when working with XA transactions.

## Repeatable Read

AKA consistent read. Achieved through snapshots.

> An important side effect of the consistent snapshots is that it is possible to have non-locking reads while still retrieving the same data repeatably.

For `SELECT`, no locks are held. For DML, some number of locks as for `SERIALIZABLE`.

Updating table in another session cascades updates to snapshots.

> If you do not need consistent reads, the READ COMMITTED transaction isolation level is a good choice .

## Read Committed

- Read view is for life of statement
- Locks taken as examination but not modified are rebased upon completion of `WHERE` clause.
- Gap locks only for FK and UK

> For WHERE clauses resolved using a non-indexed column, the semi-consistent read feature allows transactions to use the last committed values of a row to match the filter even if the row is locked.

no gaps locks implies phantom reads

`trx_sys` mutex is obtained for every read views. Higher number for `READ COMMITTED` then `REPEATABLE READ`.

For quick and frequent transactions and statements, `REPEATABLE READ` is better.

For long running transactions, `READ COMMITTED` is better.

## Read Uncommitted

Dirty read.
