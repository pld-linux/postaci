# TODO
# - webapps
Summary:	Postaci is a PHP based POP3/IMAP based e-mail client
Summary(pl.UTF-8):	Postaci jest opartym na PHP klientem pocztowym obsługującym POP3/IMAP
Name:		postaci
Version:	1.1.3
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.trlinux.com/dist/%{name}-%{version}.tar.gz
# Source0-md5:	2e2200792114c71e0fbcb820dd95e314
Source1:	%{name}-INSTALL.PLD
Source2:	%{name}.conf
Patch0:		%{name}-pld.patch
URL:		http://www.trlinux.com/
Requires:	apache(mod_auth)
Requires:	php(imap)
Requires:	php(mysql)
Requires:	webserver = apache
Requires:	webserver(php) >= 4.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_postacidir	/home/services/httpd/html/postaci

%description
Postaci is a PHP based POP3/IMAP e-mail client. It supports both
protocols and the default protocol can be changed from a single
configuration file. Postaci is platform independent. It can work on
any operating system which supports PHP. Postaci is also database
independent. It supports MySQL, mSQL, Microsoft SQL, Sybase,
PostgreSQL. It uses very complex database operations to simulate POP3
folders. Postaci is multilingual. It currently supports Dutch,
English, French, German, Italian, Norwegian, Polish, Portuguese,
Spanish, Turkish.

%description -l pl.UTF-8
Postaci jest opartym na PHP klientem pocztowym wspierającym POP3/IMAP.
Obsługuje on obydwa protokoły, a wybór domyślnego odbywa się poprzez
plik konfiguracyjny. Postaci jest niezależny od platformy. Może
działać na dowolnym systemie operacyjnym z obsługą PHP. Postaci jest
również niezależny od bazy danych. Zawiera wsparcie dla MySQL, mSQL,
Microsoft SQL, Sybase, PostgreSQL. Do symulacji skrzynek pocztowych
POP3 korzysta z bardzo skomplikowanych operacji w bazie danych.
Postaci jest wielojęzyczny. Aktualnie wspiera następujące języki:
angielski, francuski, hiszpański, holenderski, niemiecki, norweski,
polski, portugalski, turecki i włoski.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_postacidir}/{classes,images,includes,lang,tmp/{send,store},queries/UPGRADE}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd

cat >> $RPM_BUILD_ROOT%{_postacidir}/.htaccess << EOF
php_flag register_globals on
AddType application/x-httpd-php .php .php3 .phtml .inc
AddType application/x-httpd-php-source .phps
EOF

install *.php INSTALL $RPM_BUILD_ROOT%{_postacidir}
install classes/*.inc $RPM_BUILD_ROOT%{_postacidir}/classes
install images/*.{gif,psd,jpg} $RPM_BUILD_ROOT%{_postacidir}/images
install includes/*.inc $RPM_BUILD_ROOT%{_postacidir}/includes
install lang/*.inc $RPM_BUILD_ROOT%{_postacidir}/lang
install queries/{postaci-{ms,my,pg}sql-1.1,tblDomains}.sql $RPM_BUILD_ROOT%{_postacidir}/queries
install queries/UPGRADE/upgrade-mysql-1.1.{0,1}-1.1.3.sql $RPM_BUILD_ROOT%{_postacidir}/queries/UPGRADE
install %{SOURCE1} INSTALL-PLD
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/httpd/httpd.conf ] && \
	! grep -q "^Include.*/%{name}.conf" %{_sysconfdir}/httpd/httpd.conf; then
		echo "Include %{_sysconfdir}/httpd/%{name}.conf" >> %{_sysconfdir}/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
fi
echo "Before you start you have to:" >&2
zcat %{_docdir}/%{name}-%{version}/INSTALL-PLD
echo "You can find that info in %{_docdir}/%{name}-%{version}/INSTALL-PLD.gz" >&2

%preun
if [ "$1" = 0 ]; then
	umask 027
	grep -E -v "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf > \
		%{_sysconfdir}/httpd/httpd.conf.tmp
	mv -f %{_sysconfdir}/httpd/httpd.conf.tmp %{_sysconfdir}/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/{FAQ/FAQ,TODO,WHATSNEW,THANKS,INSTALL,UPGRADE}
%doc INSTALL-PLD
%defattr(640,root,http,750)
%dir %{_postacidir}
%dir %{_postacidir}/includes
%config(noreplace) %verify(not md5 mtime size) %{_postacidir}/includes/global.inc
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
%{_postacidir}/classes
%{_postacidir}/images
%{_postacidir}/includes/commonhead.inc
%{_postacidir}/includes/functions.inc
%{_postacidir}/includes/headinside.inc
%{_postacidir}/includes/javascripts.inc
%{_postacidir}/includes/stylesheets.inc
%{_postacidir}/lang
%{_postacidir}/queries
%{_postacidir}/*.php
%{_postacidir}/.htaccess
%{_postacidir}/INSTALL
%attr(770,root,http) %{_postacidir}/tmp
