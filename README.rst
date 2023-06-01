=============================
nethserver-firewall-migration
=============================

Migrate firewall configuration to NethSecurity: https://github.com/NethServer/nethsecurity

Migrate to another machine
==========================

Execute on NS7:

::

  firewall-export

Generated file can be found at :file:`/var/lib/nethserver/firewall-migration/export.tar.gz`.

Access the NethSecurity installation and upload the ``export.tar.gz`` archive using SSH,
then execute:

::

  ns-import export.tar.gz

In-place migration
==================

The ``firewall-migrate`` procedure will requires about 400MB of free disk space.
The script will:

* prepare a NethSecurity image containing the firewall export archive
* write the image to the target disk
* reboot the system with the newly installed NethSecurity

At first boot, NethSecurity will automatically import the configuration.

Test the image build process:

- execute ``firewall-migrate``
- if no error occurs, verify the ``/usr/share/nethserver-firewall-migration-builder/nethsecurity.img.gz`` file exists

To start the migration process, pass the target device as first argument:

::

  firewall-migrate /dev/vda

**NOTE**: The script will wipe the NethServer installation. The script does not ask for confirmation!

Cleanup
-------

The downloaded image is preserved to speed up multiple firewall-migrate runs.
To cleanup existing images and download a new one on next run, execute: ::

  rm -rf /usr/share/nethserver-firewall-migration-builder/


Not migrated
============

The following features will not be exported:

- Web proxy (Squid)
- Suricata
- UPS (NUT)
