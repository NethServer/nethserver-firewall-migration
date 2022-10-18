Summary: NethServer firewall migration module
Name: nethserver-firewall-migration
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
URL: %{url_prefix}/%{name}
BuildArch: noarch

Requires: nethserver-firewall-base

BuildRequires: nethserver-devtools

%description
Migrate firewall configuration to Nextsecurity.

%prep
%setup -q

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING

%changelog
