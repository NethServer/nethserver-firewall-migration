Summary: NethServer firewall migration module
Name: nethserver-firewall-migration
Version: 0.0.14
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

