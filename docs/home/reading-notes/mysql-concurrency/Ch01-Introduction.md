---
layout: default
title: 'Ch 01: Introduction'
base-url: home/reading-notes/mysql-concurrency/Ch01-Introduction.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'MySQL Concurrency'
  url: home/reading-notes/mysql-concurrency.html
---

> Often what is called a lock in MySQL is really a lock request which can be in a granted or pending state.

Lock levels:

- SQL layer:
  - user level
  - DB object level
- Storage engine layer
  - others

> The isolation level influences both which locks are taken and how long a time they are held.

MySQL Shell 8.0.2.0+

Python module: `concurrency_book.generate`

```sql
source world.sql
```

