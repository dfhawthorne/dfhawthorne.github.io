---
layout: default
title: 'Ch 04: Concurrency and Multiversioning'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch04_Concurrency_and_Multiversioning.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

multiversion:

- read consistency
- write consistency

Two phase commit can prevent read of data for a very short time.

The standard isolation levels are:

| Level | Dirty Read | non Repeatable Read | Phantom Read |
| --- | --- | --- | --- |
| Read uncommitted | Yes | Yes | Yes |
| Read committed | No | Yes | Yes |
| Repeatable read | No | No | Yes |
| Serializable | No | No | No |

- Phantom read - more rows could be returned
- non Repeatable read (RR) - row could be changed or deleted

Oracle RDBMS has:

- read committed plus non-blocking read
- serializable
- read only

> A transaction using a READ ONLY isolation level only sees those changes that were committed __at the time the transaction began__, but inserts, updates, and deletes are not permitted in this mode (other sessions may update data, but not the READ ONLY transaction).

### RR and Serialization Levels

Read committed can be bad as a dirty read.

In other RDBMS, RR is achieved through row-level shared read locks:

- readers block writers
- can cause deadlocks

RR only useful in a stateful connection.

#### SERIALIZABLE

[ORA-08177](https://docs.oracle.com/en/error-help/db/ora-08177/?r=23ai) _can't serialize access for this transaction_ (checked at block level)

Oracle uses optimistic view of serialization:

- low probability of concurrent updates
- need transaction level of read consistency
- short transactions

Used for TPC-C benchmarks

SERIALIZABLE does not imply serial ordering of transactions

```sql
ALTER SESSION SET ISOLATON_LEVEL=SERIALIZABLE;
```

A `READ ONLY` transaction could see [ORA-1555](https://docs.oracle.com/en/error-help/db/ora-01555/index.html?r=23ai).

Multiversion read consistency can cause high I/O due to block rollbacks. Oracle can use cached rolled back blocks.

- Consistent read when finding rows to modify
- Current reads when getting the block to actually update the row of interest

Why 3 current gets for an update?

> The mode gets are performed in order to retrieve the table block as it exists right now, the one with the row in it, to get an undo segment block to begin our transaction, and an undo block.

Transactions will restart silently if the current read detects a change from what was returned by a consistent. It is at this point that an [ORA-08177](https://docs.oracle.com/en/error-help/db/ora-08177/?r=23ai) occurs in `SERIALIZABLE` mode.

Restarts can be caused by having `NEW` and `OLD` values in a `BEFORE EACH ROW` trigger. This is important for triggers that do auditing, or sending messages to users via `UTL_` functions.

```sql
SELECT FOR UPDATE NOWAIT
```

prevents __LOST UPDATES__.

