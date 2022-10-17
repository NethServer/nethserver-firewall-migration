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

Access the NextSecurity installation and ``export.tar.gz`` using SSH,
then execute:

::

  ns-import export.tar.gz

In-place migration
==================

The ``firewall-migrate`` script will:

* prepare a NextSecurity image containing the firewall export archive
* write the image to the target disk
* reboot the system with the newly installed NextSecurity

Test the image build process:

- execute ``firewall-migrate``
- if no error occurs, verify the ``/usr/share/nethserver-firewall-migration-builder/nextsecurity-generic-ext4-combined-efi.img.gz`` exists

To start the migration process, pass the target device as first argument

::

  firewall-migrate /dev/vda

Not migrated
============

The following featuers will not be exported:

- Web proxy (Squid)
- Suricata
- UPS (NUT)
