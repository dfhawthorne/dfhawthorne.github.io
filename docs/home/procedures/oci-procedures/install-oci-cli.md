---
layout: default
title: Install OCI CLI
base-url: home/procedures/oci-procedures/install-oci-cli.html
breadcrumbs:
- title: 'Home'
  url: index.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'OCI Procedures'
  url: home/procedures/oci-procedures.html
file-download-dir: home/procedures/oci-procedures/install-oci-cli
file-download:
- install_oci_cli.log
---

# Install OCI CLI

## Summary

I installed the OCI CLI manually.

## References

* [Command Line Interface (CLI)](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm)
  * [Quickstart](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
    * [Linux and Unix](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#InstallingCLI__linux_and_unix)

## Procedure

### Remove Previous Installation

Run the following command to remove any previous installation:

```bash
rm -fR ~/lib/oracle-cli ~/bin/oci-cli-scripts ~/bin/oci
```

### Manual Installation

Run the following command to download and run the installer:

```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

The log is uploaded as [install_oci_cli.log](home/procedures/oci-procedures/install-oci-cli/install_oci_cli.log)

### Repair File Permissions

In order to avoid the following warning:

```text
WARNING: Permissions on /home/douglas/.oci/tenancy_admin_private.pem are too open. 
To fix this please try executing the following command: 
oci setup repair-file-permissions --file /home/douglas/.oci/tenancy_admin_private.pem 
Alternatively to hide this warning, you may set the environment variable, OCI_CLI_SUPPRESS_FILE_PERMISSIONS_WARNING: 
export OCI_CLI_SUPPRESS_FILE_PERMISSIONS_WARNING=True
```

I ran the suggested command:

```bash
oci setup repair-file-permissions --file /home/douglas/.oci/tenancy_admin_private.pem
```

### Create an OCI Session

Run the following command to create an OCI session:

```bash
oci session authenticate --no-browser --profile-name DEFAULT --region ap-sydney-1
```

### Validate OCI Session

To validate the OCI session, I ran the following command:

```bash
oci session validate
```

A sample response is:

```text
Session is valid until 2024-05-24 03:53:42
```

