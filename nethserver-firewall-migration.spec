Summary: NethServer firewall migration module
Name: nethserver-firewall-migration
Version: 1.0.4
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-cockpit.tar.gz
URL: %{url_prefix}/%{name}
BuildArch: noarch

Requires: nethserver-firewall-base
Requires: squashfs-tools

BuildRequires: nethserver-devtools

%description
Migrate firewall configuration to NethSecurity.

%prep
%setup -q

%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%{genfilelist} %{buildroot} \
    --file /etc/sudoers.d/50_nsapi_nethserver_firewall_migration 'attr(0440,root,root)' \
 > %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING

%changelog
* Thu Mar 20 2025 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.4-1
- Migration: MWAN policy issues with long and similar names - NethServer/nethsecurity#1067

* Tue Dec 17 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1
- Migration: PPPoE alias import fails with invalid argument error - NethServer/nethsecurity#913
- Migration: error during OpenVPN tunnel migration due to missing 'topology' key - NethServer/nethsecurity#889
- In-place  migrate: do not drop caches (#56)
- dhcp: improve minimum lease time

* Mon Oct 21 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1
- Migration: DHCP domain option not honoured  - Bug NethServer/nethsecurity#857
- Migration: root password authentication flag incorrectly displayed inside the UI - Bug NethServer/nethsecurity#806
- Download correct image with subscription enabled
- Do not fail export if VPN is not installed

* Wed Sep 25 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- Migration: OpenVPN Road Warrior certificate not exported if CN contains the dot char - Bug NethServer/nethsecurity#794
- Migration: FlashStart not enabled on guest/blue interface - Bug NethServer/nethsecurity#792
- Migration: rules with custom zones not correctly migrated - Bug NethServer/nethsecurity#789
- Migration: wrong zone for OpenVPN and IPSec custom rules - Bug NethServer/nethsecurity#788
- Migration: incorrect reflection_zone and IPsec settings in port forward rule - Bug NethServer/nethsecurity#787

* Tue Sep 24 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- routes: suppress warning if device is not set
- firewall-migrate: sleep before image write (#45), avoid kernel corruption on in-place upgrade
- openvpn: do not ignore users without 'status' prop coming from NS6 (#44)

* Tue Sep 03 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.21-1
- Migration: firewall rules with "Any" service migrate incorrectly as empty "Custom Service" - Bug NethServer/nethsecurity#727
- Migration: firewall rules not converted to guest zone - Bug NethServer/nethsecurity#726

* Fri Aug 23 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.20-1
- Improve LDAP configuration and authentication consistency  - NethServer/nethsecurity#627
- Fix image download URL for subscriptions (#40)

* Mon Jul 01 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.19-1
- Migration: remove gateway from non-red interfaces - Bug NethServer/nethsecurity#612
- Migration: disable multiWAN when there is only one provider - Bug NethServer/nethsecurity#613
- Enhance LDAP remote database authentication - NethServer/nethsecurity#602
- Migration: user import regression with remote AD - Bug NethServer/nethsecurity#609

* Mon Jun 03 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.18-1
- Migration: OpenVPN Road Warrior users not visible in UI after migration - Bug NethServer/nethsecurity#559

* Mon May 13 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.17-1
- UI: explain Threat shield DNS is not migrated

* Mon Apr 29 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.16-1
- OpenVPN RW: fix migration of old users without status prop

* Tue Apr 23 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.15-1
- ns-api: ipsec, create multiple children tunnels - NethServer/nethsecurity#442

* Tue Apr 16 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.14-1
- ipsec: remap hash_algorithm and salifetime (#32)
- rules: explode src and dest addresses (#33) - nethsecurity#429
    

* Thu Apr 04 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.13-1
- Improve WAN export

* Tue Mar 19 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.12-1
- Export device name/hwaddr map

* Tue Mar 05 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.11-1
- Fix image download URL
- Always download image

* Mon Feb 19 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.10-1
- SNAT: set dest_ip for the UI

* Wed Feb 14 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.9-1
- Drop disk caches before reboot

* Thu Feb 01 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.8-1
- Improve port forwarding

* Fri Jan 26 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.7-1
- Improve proxy pass export

* Thu Jan 18 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.6-1
- Improve firewall rules export

* Wed Jan 17 2024 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.5-1
- Refactor OpenVPN export
- Multiple fixes

* Wed Nov 15 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.4-1
- Improve OpenVPN roadwarrior export

* Fri Nov 10 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.3-1
- Custom image was not build due to kpartx failure

* Fri Nov 03 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.2-1
- Fixes for OpenVPN tunnels and network

