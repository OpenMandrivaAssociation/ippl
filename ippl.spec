%define name ippl
%define version 1.99.5
%define release %mkrel 9

Summary: Logs TCP, ICMP and UDP connections
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://www.via.ecp.fr/~hugo/ippl/
Source: http://pltplp.net/ippl/archive/dev/%{name}-%{version}.tar.bz2
Source2: ippl.init
Source3: ippl.log
Patch0: %{name}-log.patch
License: GPL
Group: Monitoring
Buildrequires:	libpcap-devel
Buildrequires:  byacc
Buildrequires:  flex
Buildroot: %{_tmppath}/%{name}-buildroot
Requires(pre): chkconfig

%description
ippl is a configurable IP protocols logger. It currently logs incoming ICMP
messages, TCP connections and UDP datagrams. It is configured with
Apache-like rules and has a built-in DNS cache. It is aimed to replace
iplogger.

%prep

%setup -q

%patch0 -p0 -b .log

%build

%configure --with-user=nobody

%make

%install
rm -rf $RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/%{_sysconfdir}
mkdir $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d
mkdir $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d
mkdir $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
mkdir $RPM_BUILD_ROOT/var
mkdir $RPM_BUILD_ROOT/var/log
mkdir $RPM_BUILD_ROOT/var/log/ippl

make ROOT=$RPM_BUILD_ROOT install

touch $RPM_BUILD_ROOT/var/log/ippl/all.log


install -m755 %{SOURCE2} \
              $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ippl
install -m644 %{SOURCE3} \
              $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ippl


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ippl

%preun
if [ $1 = 0 ]; then
   /sbin/chkconfig --del ippl
fi


%files
%defattr(-,root,root)
%doc BUGS CREDITS HISTORY INSTALL LICENSE README TODO
%config(noreplace) %{_sysconfdir}/ippl.conf
%config(noreplace) %{_sysconfdir}/rc.d/init.d/ippl
%config(noreplace) %{_sysconfdir}/logrotate.d/ippl
# %dir /var/log/ippl
%config /var/log/ippl/all.log
%{_mandir}/man5/ippl.conf.*
%{_mandir}/man8/ippl.*
%{_sbindir}/*



