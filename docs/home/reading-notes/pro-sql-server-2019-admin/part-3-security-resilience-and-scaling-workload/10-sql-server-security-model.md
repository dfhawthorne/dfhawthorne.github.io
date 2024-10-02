---
layout: default
title: '10. SQL Server Security Model'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/10-sql-server-security-model.html
breadcrumbs:
- title: Home
  url: index.html
- title: Reading Notes
  url: home/reading-notes.html
- title: 'Pro SQL Server 2019 Adminstration'
  url: home/reading-notes/pro-sql-server-2019-admin.html
- title: 'Part III. Security Resilience and Scaling Workload'
  url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload
---

The hierarchy of security is:

- Domain
  - Server
    - Instance
      - Database

Unless using a contained database, all users be authenticated at the instance level. Windows (preferred) versus Mixed Mode.

Can grant access through groups or users

SID (Security Identifier) in MDB

Certificates/asynchronous keys used for code signing

Mixed mode has special user, `SA` (system adminstrator on entire instance)

```sql
ALTER LOGIN sa WITH NAME=N'new_admin';
```

User password: second tier authentication is less secure than Windows authentication.

## Server Roles

| Server Role | Description |
| --- | --- |
| `sysadmin` | full rights |
| `bulkadmin` | need `INSERT` rights. Can use `BULK INSERT` |
| `dbcreator` | can `CREATE DATABASE` then becomes `DBOWNER` |
| `diskadmin` | manage backup devices |
| `processadmin` | can stop instance. kill running processes |
| `public` | default for logins |
| `securityadmin` | manage login at instance level only. Cannot add `sysadmin`. Cannot manage permissions in database |
| `serveradmin` | = `diskadmin` + `processadmin` + start/stop instance with `SHUTDOWN` but without `CHECKPOINT` and `NOWAIT`. `ALTER ENDPOINTS`. Can view all instance metadata |
| `setupadmin` | create and manage linked servers |

```sql
CREATE SERVER ROLE r AUTHORIZAION [domain\user];
```

Default database: cannot login if

- database dropped
- no permissions on database

```sql
USE MASTER
CREATE LOGIN l WITH PASSWORD=pw;
USE db
CREATE USER l FOR LOGIN l;
USE MASTER
CREATE LOGIN [domain\user] FROM WINDOWS WITH DEFAULT_DATABASE=db;
USE db
CREATE USER [domain\user] FOR LOGIN [domain\user];
```

`DENY` overrides `GRANT` e.g. `GRANT` to group, `DENY` principal means principal is denied

`DENY` requires `[Object class]::[securable]`

```sql
GRANT ALTER ANY LOGIN TO user;
DENY ALTER ON LOGIN::[domain\user] TO user;
```

## Database Roles

Role Name | Description
--- | ---
`db_accessadmin` | add/remove users

