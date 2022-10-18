# Disable strip, debuginfo and python compile
%global __os_install_post %{nil}
%global debug_package %{nil}

%define nextsec_ver 22.03.0
Summary: NethServer firewall migration module
Name: nethserver-firewall-migration
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: https://nextsec-testing.fra1.digitaloceanspaces.com/targets/x86/64/nextsecurity-imagebuilder-%{nextsec_ver}-x86-64.Linux-x86_64.tar.xz
Source2: https://github.com/NethServer/nextsecurity/archive/refs/heads/master.tar.gz
URL: %{url_prefix}/%{name}
AutoReq: no

Requires: nethserver-firewall-base
Requires: perl-Thread-Queue devtoolset-7-make git unzip bzip2

BuildRequires: nethserver-devtools

%description
Migrate firewall configuration to Nextsecurity.

%prep
%setup -q

%build
perl createlinks
mkdir -p root/usr/share/nethserver-firewall-migration-builder
tar xvf %{SOURCE1} -C root/usr/share/nethserver-firewall-migration-builder --strip-components=1
cd root/usr/share/nethserver-firewall-migration-builder
tar xvf %{SOURCE2} nextsecurity-master/files/; mv nextsecurity-master/files/ .; rmdir nextsecurity-master
sed -i '/logd \\/d' include/target.mk

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} | grep -v -e '\.pyo$' -e '\.pyc$'> %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING

%changelog
