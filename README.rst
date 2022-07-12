=============================
nethserver-firewall-migration
=============================

Migrate firewall configuration to NextSecurity: https://github.com/NethServer/nextsecurity

How to use it
=============

Execute on NS7:

::

  firewall-export

Generated file can be found at :file:`/var/lib/nethserver/firewall-migration/export.tar.gz`.

Upload the ``export.tar.gz`` to Nextsecurity and execute:

::

  firewall-import export.tar.gz

Not migrated
============

The following configurations will not be migrated:

- Web proxy (Squid)
- Suricata
