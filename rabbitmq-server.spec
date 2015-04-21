%define		uid	257
%define		gid	257
Summary:	Implementation of an AMQP broker
Name:		rabbitmq-server
Version:	3.5.0
Release:	1
License:	MPL v1.1
Group:		Applications/Communications
Source0:	http://www.rabbitmq.com/releases/rabbitmq-server/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e599837e6d6984781a6b93b90d3b7edc
Source1:	rabbitmq.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.service
Patch0:		rabbitmqctl-no_root.patch
URL:		http://www.rabbitmq.com/
BuildRequires:	docbook-dtd45-xml
BuildRequires:	erlang
BuildRequires:	erlang-sd_notify
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	xmlto
Requires(post,preun):	/sbin/chkconfig
Requires:	erlang
Requires:	erlang-sd_notify
Requires:	rc-scripts
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RabbitMQ provides robust messaging for applications. It is easy to
use, fit for purpose at cloud scale and supported on all major
operating systems and developer platforms.

%prep
%setup -q

%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{lib,log}/rabbitmq,/etc/{sysconfig,rc.d/init.d,rabbitmq},%{systemdunitdir}}

%{__make} install \
	TARGET_DIR=$RPM_BUILD_ROOT%{_libdir}/%{name} \
	SBIN_DIR=$RPM_BUILD_ROOT%{_sbindir} \
	MAN_DIR=$RPM_BUILD_ROOT%{_mandir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{INSTALL,LICENSE*}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rabbitmq/rabbitmq-env.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g %{gid} rabbitmq
%useradd -u %{uid} -s /bin/sh -d /var/lib/rabbitmq -g rabbitmq -c "RabbitMQ Server" rabbitmq

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 3.5.0
%systemd_trigger %{name}.service

%files
%defattr(644,root,root,755)
%doc README
%dir %{_sysconfdir}/rabbitmq
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rabbitmq/rabbitmq-env.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rabbitmq-server
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/rabbitmq-server.service
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
