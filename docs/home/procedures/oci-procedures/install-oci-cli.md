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
- 'install_oci_cli.log'
---

# Install OCI CLI

## Summary

I installed the OCI CLI manually.

## References

* [Command Line Interface (CLI)](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm)
  * [Quickstart](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
    * [Linux and Unix](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm#InstallingCLI__linux_and_unix)
  * [Token-based Authentication for the CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clitoken.htm)
    * [Creating a CLI Session without a Browser](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clitoken.htm#clitoken_topic-Starting_a_Tokenbased_CLI_Session_No_Browser)
  * [Configuring the CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm)
    * [CLI Configuration File](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm#CLIconfigfile)
    * [Specifying a Default Profile](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm#Specifying_a_Default_Profile)
  * [CLI Environment Variables](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clienvironmentvariables.htm)

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

### Create OCI CLI Configuration File

Following the procedure in "[CLI Configuration File](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm#CLIconfigfile)", I ran the following command to create the OCI CLI configuration file (`~/.oci/oci_cli_rc`):

```bash
oci setup oci-cli-rc --file ~/.oci/oci_cli_rc
```

The expected output is:

```text
Predefined queries written under section OCI_CLI_CANNED_QUERIES
Command aliases written under section OCI_CLI_COMMAND_ALIASES
Parameter aliases written under section OCI_CLI_PARAM_ALIASES
```

### Set OCI CLI Default Profile

In order to have the OCI CLI co-exist with Ansible, the OCI CLI has to use a different profile, `OCI`.

Following the procedure in "[Specifying a Default Profile](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm#Specifying_a_Default_Profile)", the following two (2) lines are added to the OCI CLI configuration file, `~/.oci/oci_cli_rc`:

```text
[OCI_CLI_SETTINGS]
default_profile=OCI

[OCI]
# for the OCI profile
```

__NOTE:__ Do not add `endpoint` to the `[OCI]` profile as this uses this endpoint as default for all OCI calls.

### Create an OCI Session

Following the procedure in "[Creating a CLI Session without a Browser](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clitoken.htm#clitoken_topic-Starting_a_Tokenbased_CLI_Session_No_Browser)", run the following command to create an OCI session:

```bash
oci session authenticate --no-browser --profile-name OCI --region ap-sydney-1
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

### Update .zshrc and .bashrc

Update both `~/.zshrc` and `~/.bashrc` with the following lines:

```text
export OCI_CLI_TENANCY="ocid1.tenancy.oc1..aaaaaaaa7ilqdzmkbqduujc3tt6zrl2n2ytcughcjoidozg4memj2k4cm7na"
export OCI_CLI_AUTH=security_token
export OCI_CLI_REGION=ap-sydney-1
```

Other environment variables can be found at "[CLI Environment Variables](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clienvironmentvariables.htm)".
