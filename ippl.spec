Summary:	Logs TCP, ICMP and UDP connections
Name:		ippl
Version:	1.99.5
Release:	14
License:	GPL
Group:		Monitoring
URL:		http://www.via.ecp.fr/~hugo/ippl/
Source0:	http://pltplp.net/ippl/archive/dev/%{name}-%{version}.tar.bz2
Source1:	%{name}.service
Source2:	%{name}.log
Patch0:		%{name}-log.patch
Patch1:		ippl-1.99.5.printf.patch
Patch2:		ippl-1.99.5.nostrip.patch
Requires(pre): 	chkconfig
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Buildrequires:	libpcap-devel
Buildrequires:	byacc
Buildrequires:	flex

%description
ippl is a configurable IP protocols logger. It currently logs incoming ICMP
messages, TCP connections and UDP datagrams. It is configured with
Apache-like rules and has a built-in DNS cache. It is aimed to replace
iplogger.

%prep

%setup -q

%patch0 -p0 -b .log
%patch1 -p1 -b .printf
%patch2 -p1 -b .nostrip

%build
%configure --with-user=nobody
%make

%install
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var
install -d %{buildroot}/var/log
install -d %{buildroot}/var/log/ippl

make ROOT=%{buildroot} install

touch %{buildroot}/var/log/ippl/all.log

install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/ippl

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc BUGS CREDITS HISTORY INSTALL LICENSE README TODO
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/ippl.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/ippl
# %dir /var/log/ippl
%config /var/log/ippl/all.log
%{_mandir}/man5/ippl.conf.*
%{_mandir}/man8/ippl.*
%{_sbindir}/*
