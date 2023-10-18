# Disable strip, debuginfo and python compile
%global __os_install_post %{nil}
%global debug_package %{nil}

%define nethsec_ver 23.05.0
Summary: NethServer firewall migration module
Name: nethserver-firewall-migration
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-cockpit.tar.gz
Source2: https://github.com/NethServer/nethsecurity/archive/refs/tags/%{nethsec_ver}.tar.gz
Source3: https://updates.nethsecurity.nethserver.org/%{nethsec_ver}/targets/x86/64/nethsecurity-imagebuilder-%{nethsec_ver}-x86-64.Linux-x86_64.tar.xz
URL: %{url_prefix}/%{name}
AutoReq: no

Requires: nethserver-firewall-base
Requires: perl-Thread-Queue devtoolset-7-make git unzip bzip2

BuildRequires: nethserver-devtools

%description
Migrate firewall configuration to NethSecurity.

%prep
%setup -q

%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json
mkdir -p root/usr/share/nethserver-firewall-migration-builder
tar xvf %{SOURCE3} -C root/usr/share/nethserver-firewall-migration-builder --strip-components=1
cd root/usr/share/nethserver-firewall-migration-builder
tar xvf %{SOURCE2} nethsecurity-%{nethsec_ver}/files; mv nethsecurity-%{nethsec_ver}/files/ .; rmdir nethsecurity-%{nethsec_ver}
sed -i '/logd \\/d' include/target.mk

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
    | grep -v -e '\.pyo$' -e '\.pyc$' \
 > %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING

%changelog
