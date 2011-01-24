%define		uid	257
%define		gid	257
Summary:	Implementation of an AMQP broker
Name:		rabbitmq-server
Version:	2.1.1
Release:	0.10
License:	MPL v1.1
Group:		Applications/Communications
Source0:	http://www.rabbitmq.com/releases/%{name}/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2359d4b90431925e971726a6e0274bf8
Source1:	rabbitmq.conf
Source2:	%{name}.init
URL:		http://www.rabbitmq.com
BuildRequires:	erlang
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	xmlto
BuildRequires:	docbook-dtd45-xml
Requires:		erlang
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

%{__make} install \
		TARGET_DIR=$RPM_BUILD_ROOT/%{_datadir}/%{name} \
		SBIN_DIR=$RPM_BUILD_ROOT/%{_sbindir} \
		MAN_DIR=$RPM_BUILD_ROOT/%{_mandir} \

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rabbitmq/
install -d $RPM_BUILD_ROOT/var/lib/rabbitmq
install -d $RPM_BUILD_ROOT/var/log/rabbitmq
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rabbitmq/rabbitmq.conf
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -r -g %{gid} rabbitmq
%useradd -r -u %{uid} -s /bin/sh -d /var/lib/rabbitmq -g rabbitmq -c "RabbitMQ Server" rabbitmq

%post
/sbin/chkconfig --add rabbitmq-server

%files
%defattr(644,root,root,755)
%doc LICENSE README LICENSE-MPL-RabbitMQ
%config(noreplace) %verify(not md5 mtime size) /etc/rabbitmq/rabbitmq.conf
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ebin
%dir %{_datadir}/%{name}/include
%dir %{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/sbin
%{_datadir}/%{name}/ebin/*
%{_datadir}/%{name}/include/*
%{_datadir}/%{name}/plugins/*
%attr(755,root,root) %{_datadir}/%{name}/sbin/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%attr(755,rabbitmq,rabbitmq) /var/lib/rabbitmq
%attr(755,rabbitmq,rabbitmq) /var/log/rabbitmq
