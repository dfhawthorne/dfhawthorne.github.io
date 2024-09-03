---
layout: default
title: 'Ch 05: Lock Access Levels'
base-url: home/reading-notes/mysql-concurrency/Ch05-Lock-Access-Levels.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

distinct from lock granularity

Intention locks

### Shared Locks

Shared lock on table while reading.

No shared data lock unless `SERIALIZABLE` or through `FOR SHARE` or `LOCK IN SHARE MODE`.

### Exclusive Locks

DDL/DML

`UPDATE`

- `SHARED_WRITE` on table
- `SHARED_READ` on parent

metadata locks

data locks

- `IX` (Insert exclusive) on table
- `X REC_NOT_GAP` (Exclusive) on row

### Lock Compatability

> Two intention locks are always compatible with each other. This means that even if a transaction has an intention exclusive lock, it will not prevent another transaction to take an intention lock. It will however stop the other transaction from upgrading its intention lock to a full lock.

|     | `X` | `IX` | `S` | `IS` |
| --- | --- | ---  | --- | ---  |
| `X` | No | No | No | No |
| `IX` | No | Yes | No | Yes |
| `S` | No | No | Yes | Yes |
| `IS` | No | Yes | Yes | Yes |


