---
layout: default
title: 'Ch 05: Transactions'
base-url: home/reading-notes/oracle-database-transactions-and-locking-revealed/Ch05_Transactions.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Oracle Database Transactions and Locking Revealed'
  url: home/reading-notes/oracle-database-transactions-and-locking-revealed
---

Transactions take the database from one consistent state to another.

Can begin a transaction with:

- `SET TRANSACTION`
- `DBMS_TRANSACTION` package

Implicitly started by first DML

Transaction control statements:

- `COMMIT`
- `ROLLBACK`
- `SAVEPOINT`
- `ROLLBACK TO sp`
- `SET TRANSACTION`

Statements are implicitly wrapped in _Savepoints_. Rollbacks to that savepoint are done if the statement fails.

PL/SQL blocks are considered statements.

It is bad programming to do `COMMIT` or `ROLLBACK` inside a PL/SQL program.

```sql
WHEN OTHERS
    RAISE;
```

or use `RAISE_APPLICATION_ERROR`

```sql
ALTER SESSION SET plsql_warnings='enable:all';
```

DDL always commits

### Write Extensions to COMMIT

10G R2+

Normally `COMMIT` is synchronous (a physical I/O to disk)

```sql
COMMIT WRITE NOWAIT
```

Used for:

- batch processes
- restartable operations

PL/SQL does asynchronous commits:

- non-distributed only
- before exit, `COMMIT WRITE NOWAIT` is done

### Constraints

`IMMEDIATE` - checked immediately after entire SQL statement has been processed.

SQL not PL/SQL

`DEFERRABLE` e.g. cascadable update of PK in parent

In a child table, use:

```sql
FOREIGN KEY CONSTRAINT child_fk
    REFERENCES parent(pk)
    DEFERRABLE
    INITIALLY IMMEDIATE
```

Most applications do not check for constraint violations on `COMMIT`.

```sql
SET CONSTRAINT child_fk DEFERRED;
...
SET CONSTRAINT child_fk IMMEDIATE;
```

Do not create all constraints as deferrable as PK and UK indexes would be structured differently to allow for non-uniqueness.

`NOT NULL DEFERRABLE` is treated by CBO as NULLABLE.

Data integrity determines transaction boundaries.

Restartable processes require complex logic.

Simplicity: SQL, PL/SQL

Autocommit is __BAD__!

### Distributed Transactions

In-doubt distributed transaction

Over DB link, no `COMMIT`, DDL, `SAVEPOINT`.

`COMMIT_POINT_STRENGTH` increases probability of becoming transaction controller.

### Autonomous Transactions

Autonomous transactions should be rare!

```sql
PRAGMA AUTONOMOUS_TRANSACTION;
```

Only valid use is to log errors.

> Data integrity drives the transaction size.

