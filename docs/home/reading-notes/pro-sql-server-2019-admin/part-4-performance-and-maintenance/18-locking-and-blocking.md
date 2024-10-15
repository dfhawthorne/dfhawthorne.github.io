---
layout: default
title: '18. Locking and Blocking'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-4-performance-and-maintenance/18-locking-and-blocking.html
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

Locking granularity:

- `RID`/`KEY`
- `PAGE`
- `EXTENT` (8 contiguous pages)
- `HoBT` (heap or B-Tree)
- `TABLE` (include indexes)
- `FILE`
- `METADATA`
- `ALLOCATION_UNIT`
- `DATABASE`

Lock includes intent lock on next level i.e. `RID`/`KEY` lock also gets an intent lock on the page.

```text
LOCK_ESCALATION TABLE
                AUTO
                DISABLE

MAX_DURATION (in minutes)
ABORT_AFTER_LIMIT NONE
                  SELF
                  BLOCKERS
WAIT_AT_COW_PRIORITY is equivalent to
    MAX_DURATION      = 0 &
    ABORT_AFTER_WAIT  = NONE
```

Lock partitioning #cores \> 16 reduces lock contention

Deadlock monitor kills process with lowest transaction priorities. If same priority, kill one with least resource utilisation. If same priority and resource utilisaion, kill one at random.

Guidelines for deadlock minimisation:

- Optimistic locking levels
- no user interaction for transactions
- short transactions
- access resource in same order

Understanding Transaction:

- Autocommit
- Explicit: `BEGIN TRANSACTION`
- Implicit: autocommit off, ended by `COMMIT`/`ROLLBACK`
- Savepoint - everything before is committed. Everything after is either committed or rolled back.

## Consistency

```sql
ALTER TABLE t WITH CHECK
  CHECK CONSTRAINT ALL;
```

## Isolation

- Dirty Read - data never existed
- Repeatable Read - same row different values
- Phantom Read - new rows appear in second read

Pessimistic:

- Read uncommitted
- Read committed (default)
- Serializable

Optimistic:

- Row versioning
- Snapshot isolation
- Read Committed snapshot

```text
sys.databases
  name
  snapshot_isolation_state_desc='OFF'
  is_read_committed_snapshot_on=0

sys.dm_exec_sessions
  database_id = DB_ID('db')
```

```sql
ALTER DATABASE db SET
  ALLOW_SNAPSHOT_ISOLATION ON,
  READ_COMMITTED_SNAPSHOT ON;
```

## Durability

delayed durability - in log buffer until

- buffer full
- fully durable transaction commits
- `sp_flush_log`

```sql
ALTER DATABASE db SET
  DELAYED_DURABILITY = [ALLOWED|FORCE|DISABLED (default)];
...
COMMIT WITH (DELAYED_DURABILITY=ON);
```

Deferred transaction stops VLF truncation

## Transaction with In-Memory OLTP

Memory optimised tables have no support for locks to imprive concurrency.

Optimistic isolation levels - row versioning (not in TempDB)

Read committed N/A for explicit/implicit transaction, nor in ATOMIC block of natively complied store procedure.

`MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT`

Autocommit:

- Read committed
- Read committed snapshot

Repeatable Read only in ATOMIC block in natively compiled stored procedure

Serializable = Repeatable Read + no new rows in transaction query

```sql
BEGIN TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
...
COMMIT;
```

## Observing Transactions, Locsk and Deadlocks

```text
sys.dm_tran_active_transactions
sys.dm_tran_session_transactions
sys.dm_dm_exec_sessions
sys.dm_exec_requests
sys.dm_exec_sql_text(hdl)

sys.dm_tran_locks

sys.dm_os_waiting_tasks
```

Deadlocks trace flag

- 1204 - details of resource and types of locks involved in deadlock
- 1222 - victim, process, resources involved in deadlock

Not needed as data is available in System Health session. On by default

Management \> External Event \> Session \> System Health
