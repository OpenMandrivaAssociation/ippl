Summary:	Logs TCP, ICMP and UDP connections
Name:		ippl
Version:	1.99.5
Release:	%mkrel 12
License:	GPL
Group:		Monitoring
URL:		http://www.via.ecp.fr/~hugo/ippl/
Source0:		http://pltplp.net/ippl/archive/dev/%{name}-%{version}.tar.bz2
Source2:	ippl.init
Source3:	ippl.log
Patch0:		%{name}-log.patch
patch1:		ippl-1.99.5.printf.patch
patch2:		ippl-1.99.5.nostrip.patch
Requires(pre): chkconfig
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


%changelog
* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.99.5-12mdv2009.1
+ Revision: 298262
- rebuilt against libpcap-1.0.0

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.99.5-11mdv2009.0
+ Revision: 239035
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 23 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.99.5-10mdv2008.0
+ Revision: 70274
- kill file require on chkconfig


* Fri Jul 29 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.99.5-8mdk
- Fix BuildRequires

* Thu Jul 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1.99.5-7mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Thu Jul 07 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.99.5-6mdk
- rebuild

* Thu May 27 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.99.5-5mdk
- rebuild

