---
layout: default
title: 'Ch 09: Troubleshooting'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch09_Troubleshooting.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

Unindexed FK

- `ON DELETE CASCADE` locks child table
- Join from child to parent

Killing session:

- status = 'terminated' if rollback > 1 min
- `IMMEDIATE` -> return to user after kill without waiting for completion or time-out of 1 min

18C+ `ALTER SYSTEM CANCEL`

SQL `<sid>,<serial>[,@<instance>][,<sql_id>]`

[ORA-54](https://docs.oracle.com/en/error-help/db/ora-00054/?r=23ai) `DDL_LOCK_TIMEOUT`

