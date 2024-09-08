---
layout: default
title: 'Ch 10: Indexes and Foreign Keys'
base-url: home/reading-notes/mysql-concurrency/Ch10-Indexes-and-Foreign-Keys.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

Locks consume memory in buffer pool.

## Primary versus Secondary Indexes

> The most effective way to access a row is by its primary key as that ensures just the rows that are affected by the statement are accessed.

Instead of using a secondary key to do DML, use secondary key to determine PK, then use PK to do DML. But be aware that PK of selected row may change in the meantime.

## Ascending versus Descending Indexes

MySQL 8+ Descending Indexes

INNODB appends PK to end of a non-unique key in order to generate a UK.

Descending index gives performance gain in sequential access and feewr gap locks.

## Unique Indexes

Reduces number of locks over non-unique.

## Foreign Keys

No shared metadata lock on child when inserting into parent.

Extra locks are tkaen if FK columns are changed.

Cascading relations can cause the number of metadata locls to increase quickly.

## DDL Statement

DDL against tables with FK: `SHARED_UPGRADABLE` metadata lock against parents and children of modified tables.
