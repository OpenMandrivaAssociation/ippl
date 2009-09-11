Summary:	Logs TCP, ICMP and UDP connections
Name:		ippl
Version:	1.99.5
Release:	%mkrel 13
License:	GPL
Group:		Monitoring
URL:		http://www.via.ecp.fr/~hugo/ippl/
Source:		http://pltplp.net/ippl/archive/dev/%{name}-%{version}.tar.bz2
Source2:	ippl.init
Source3:	ippl.log
Patch0:		%{name}-log.patch
Requires(pre): chkconfig
Buildrequires:	libpcap-devel
Buildrequires:	byacc
Buildrequires:	flex
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var
install -d %{buildroot}/var/log
install -d %{buildroot}/var/log/ippl

make ROOT=%{buildroot} install

touch %{buildroot}/var/log/ippl/all.log

install -m755 %{SOURCE2} %{buildroot}%{_initrddir}/ippl
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/ippl

%post
/sbin/chkconfig --add ippl

%preun
if [ $1 = 0 ]; then
   /sbin/chkconfig --del ippl
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS CREDITS HISTORY INSTALL LICENSE README TODO
%{_initrddir}/ippl
%config(noreplace) %{_sysconfdir}/ippl.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/ippl
# %dir /var/log/ippl
%config /var/log/ippl/all.log
%{_mandir}/man5/ippl.conf.*
%{_mandir}/man8/ippl.*
%{_sbindir}/*
