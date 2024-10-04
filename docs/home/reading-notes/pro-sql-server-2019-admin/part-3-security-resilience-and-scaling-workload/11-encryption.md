---
layout: default
title: '11. Encryption'
base-url: home/reading-notes/pro-sql-server-2019-admin/part-3-security-resilience-and-scaling-workload/11-encryption.html
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

DPAPI Windows Data Protection API

Service Master Key created automatically with instance.

Creation - stored in mDB

- 2012+ Symmetric AES 256
- older 3DES

Upgrade from earlier versions require regeneration of Service Master Key as a best practice.

```sql
ALTER SERVICE MASTER KEY REGENERATE;
BACKUP SERVICE MASTER KEY TO FILE='fn' ENCRYPTION BY PASSWORD pw;

RESTORE SERVICE MASTER KEY FROM FILE='fn' DECRYPTION BY PASSWORD pw;
```

Avoid `FORCE` as failing re-keying loses access to data.

Database Master Key: Symmetric AES 256. Encrypts private keys and certificates.

```sql
USE db;
CREATE MASTER KEY ENCRYPTION BY PASSWORD pw;
BACKUP MASTER KEY TO FILE='fn' ENCRYPTION BY PASSWORD pw;

RESTORE MASTER KEY FROM FILE='fn'
    DECRYPTION BY PASSWORD pw1
    ENCRYPTION BY PASSWORD pw2;
```

EKM: Extensible Key Management via MSCAPI (Microsoft Cryptographic API) to SQL/Server.

## Transparent Data Encryption

TDE versus cell level encryption:

- no bloat
- less performance overhead
- transparent to applications

In-memory and `FILESTREAM` not encrypted in file group.

Bad practice to use full-text index with TDE.

Enable TDE manually for replication.

TDE causes `TEMPDB` to use TDE. TDE prevents instant file initialisation.

TDE needs:

- DB Master Key
- Create certificate which must be encrypted using DB Master Key (password no allowed)
- Create DB encryption key

2019+ `ALTER DATABSE SET ENCRYPTION [SUSPEND|RESTART]`

TDE fails on Read-Only file group. While TDE scan is in progress, cannot:

- drop file, file group, or database
- detach database
- offline database
- setting database read-only

## Managing Cell-Level Encryption

`VARBINARY(8000)`

Whole value subsitution attack thwarted by authenticator column (a.k.a salt) - usually PK

- never update authenticator column else lose access to data.

- 2016+ Always encrypted
- 2019+ Secure enclaves

Keys are stored externally

Attestation server validates secure enclave to key manager.

Secure enclaves stored uncrypted data for performance improvement.

Secure Enclaves - CNG only

Deterministic - always same cyphertext for a given plaintext - allows equality, grouping, indexing.

Randomised - more secure, more functionality

```text
sys.column_master_keys
sys.column_encryption_keys
sys.column_key_values
```

Cannot toggle between enclave enabled, and not. Can rotate keys - enclave enabled to not.

After re-encryptyin, need to do key cleanup.
