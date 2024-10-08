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

| Role Name | Description |
| --- | --- |
| `db_accessadmin` | add/remove users |
| `db_backupoperator` | for native backup. Backup tools usually require `sysadmin` |
| `db_datareader` | `SELECT ANY TABLE` |
| `db_datawriter` | DML against `ANY TABLE` |
| `db_denydatawriter` | Opposite to `db_datawriter` |
| `db_denydatareader` | Opposite to `db_datareader` |
| `db_ddladmin` | DDL against `ANY TABLE` |
| `db_owner` | Everything restricted by `DENY` |
| `db_securityadmin` | DCL except `db_owner` |

`system` -> `dbo`

```sql
USE db;
CREATE ROLE r AUTHORIZATION dbo;
ALTER ROLE r ADD MEMBER m;
GRANT SELECT ON dbo.t TO r;
DENY dml;
```

Use `DENY` sparingly.

## Schemas

2005+ user now owns a schema

Permissions on schema:

```sql
USE db;
CREATE SCHEMA s;
GRANT SELECT ON SCHEMA::s TO u;
ALTER SCHEMA s TRANSFER obj;
```

## Contained Database

User not mapped to a login. Database is easier to move between Availability Group.

| Level | Description |
| --- | --- |
| `NONE` | Default |
| `PARTIAL` | Metadata within database. Logins can use database. |
| `FULL` | Not yet implemented |

Needs to be enabled:

- server through `sp_configure`
- database through `ALTER DATABASE`

```sql
USE MASTER;
RECONFIGURE;
EXEC sp_configure 'contained database authentication' '1'
RECONFIGURATION WITH OVERRIDE
ALTER DATABASE db SET CONTAINMENT=PARTIAL WITH NO_WAIT;
CREATE USER u WITH PASSWORD=pw DEFAULT_SCHEMA=dbo;

CREATE DATABASE db;
ALTER DATABASE db SET CONTAINMENT=PARTIAL WITH NO_WAIT;
USE db;
CREATE USER u WITH PASSWORD=pw SID=s;
SELECT sid s FROM sys.databse_principals WHERE name='u';

ALTER DAtABASE db SET TRUSTWORTHY ON;
```

Can access via `GUEST` account.

## Implementing Object-Level Security

```sql
GRANT SELECT ON OBJECT::obj TO u;
```

Can drop `OBJECT::` prefix

```sql
GRANT SELECT ON t(col) TO u;
```

## Server Audit

Can log to a file - rotate, maximum size

```sql
USE MASTER;
CREATE SERVER AUDIT a
  TO FILE(
    FILEPATH='...',
    MAXSIZE=nMB,
    MAX_ROLLOVER_FILES=n,
    RESERVE_DISK_SPACE=OFF
  )
  WITH (
    QUEUE_DELAY=t,
    ON_FAILUER=CONTINUE
  )
  WHERE object_name='sysadmin';
CREATE SERVER AUDIT SPECIFICATION spe
  FOR SERVER AUDIT a
  ADD (
    SERVER_ROLE_MEMBER_CHAnGE_GROUP
  );
ALTER SERVER AUDIT a
  WITH (
    STATE=ON
  );
ALTER SERVER AUDIT SPECIFICATION spe
  WITH (
    STATE=ON
  );
```

- `sys.dm_audit_class_type_map`
- `sys.dm_audit_actions`

```sql
USE db;
CREATE DATABASE AUDIT SPECIFICATION spe
  FOR SERVER AUDIT a
  ADD (INSERT ON ... BY PUBLIC),
  ADD (...);
ALTER DATABASE AUDIT SPECIFICATION spe
  WITH (
    STATE=ON
  );
EXECUTE AS USER='u';
REVERT;
/* AUDIT_CHANGE_GROUP */
```

- Tasks
  - Data Discovery and Classification
    - Classify Data
  - Vulverability Assessment
    - Scan for Vulnerabilities
