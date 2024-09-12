---
layout: default
title: 'Ch 15: Case Study: Record Level Locks'
base-url: home/reading-notes/mysql-concurrency/Ch15-Case-Study-Record-Level-Locks.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

## The Symptoms

- __Severe__: timeoute; deadlocks
- __Mild__: slow down

_Query Analysis_ in _MySQL Enterprise Monitor_.

`sys.innodb_lock_waits`

## The Cause

- DML
- `SELECT FOR SHARE`
- `SELECT FOR UPDATE`

## The Investigation

For MySQL 8+

- `data_locks`
- `data_lock_waits`

## The Solution

Be wary of killing transaction as rollbacks have a large impacts.

## The Prevention

`READ COMMITTED`
