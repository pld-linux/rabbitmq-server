%define		uid	257
%define		gid	257
Summary:	Implementation of an AMQP broker
Name:		rabbitmq-server
Version:	2.4.1
Release:	0.2
License:	MPL v1.1
Group:		Applications/Communications
Source0:	http://www.rabbitmq.com/releases/%{name}/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6db31b4353bd44f8ae9b6756b0a831e6
Source1:	rabbitmq.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
URL:		http://www.rabbitmq.com/
BuildRequires:	docbook-dtd45-xml
BuildRequires:	erlang
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
Requires(post,preun):	/sbin/chkconfig
Requires:	erlang
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RabbitMQ provides robust messaging for applications. It is easy to
use, fit for purpose at cloud scale and supported on all major
operating systems and developer platforms.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{lib,log}/rabbitmq,/etc/{sysconfig,rc.d/init.d,rabbitmq}}

%{__make} install \
	TARGET_DIR=$RPM_BUILD_ROOT%{_libdir}/%{name} \
	SBIN_DIR=$RPM_BUILD_ROOT%{_sbindir} \
	MAN_DIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rabbitmq/rabbitmq-env.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g %{gid} rabbitmq
%useradd -u %{uid} -s /bin/sh -d /var/lib/rabbitmq -g rabbitmq -c "RabbitMQ Server" rabbitmq

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%dir /etc/rabbitmq
%config(noreplace) %verify(not md5 mtime size) /etc/rabbitmq/rabbitmq-env.conf
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/ebin
%{_libdir}/%{name}/include
%{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/sbin
%attr(755,root,root) %{_libdir}/%{name}/sbin/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%attr(750,rabbitmq,rabbitmq) /var/lib/rabbitmq
%attr(750,rabbitmq,rabbitmq) /var/log/rabbitmq
