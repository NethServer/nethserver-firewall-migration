=============================
nethserver-firewall-migration
=============================

Migrate firewall configuration to NextSecurity: https://github.com/NethServer/nextsecurity

Migrate to another machine
==========================

Execute on NS7:

::

  firewall-export

Generated file can be found at :file:`/var/lib/nethserver/firewall-migration/export.tar.gz`.

Access the NextSecurity installation and upload the ``export.tar.gz`` archive using SSH,
then execute:

::

  ns-import export.tar.gz

In-place migration
==================

The ``firewall-migrate`` procedure will requires about 510MB of free space.
The script will:

* prepare a NextSecurity image containing the firewall export archive
* write the image to the target disk
* reboot the system with the newly installed NextSecurity

Test the image build process:

- execute ``firewall-migrate``
- if no error occurs, verify the ``/usr/share/nethserver-firewall-migration-builder/nextsecurity-generic-ext4-combined-efi.img.gz`` exists

To start the migration process, pass the target device as first argument:

::

  firewall-migrate /dev/vda

**NOTE**: The script will wipe the NethServer installation. The script does not ask for confirmation!

Not migrated
============

The following features will not be exported:

- Web proxy (Squid)
- Suricata
- UPS (NUT)
