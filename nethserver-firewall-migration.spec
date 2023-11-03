Summary: NethServer firewall migration module
Name: nethserver-firewall-migration
Version: 0.0.2
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
* Fri Nov 03 2023 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.0.2-1
- Fixes for OpenVPN tunnels and network

