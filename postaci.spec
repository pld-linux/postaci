Summary:	Postaci is a PHP based POP3/IMAP based e-mail client
Name:		postaci
Version:	1.1.3
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.trlinux.com/dist/%{name}-%{version}.tar.gz
Patch0:		postaci-pld.patch
URL:		http://www.trlinux.com/
Requires:	webserver
Requires:	apache-mod_auth
Requires:	php >= 4.1.0
Requires:	php-imap
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_postacidir	/home/services/httpd/html/postaci

%description
Postaci is a PHP based POP3/IMAP based e-mail client. It can handle
both protocols and the defaul protocol can be changed from a single
configuration file. Postaci is platform independent. It can work on
any operating system which PHP supports. Postaci is also database
independent. It can handle with MySQL, mSQL, Microsoft SQL, Sybase,
PostgreSQL. It uses very complicated database operations for handling
with POP3 folder simulation. Postaci is multilanguage. It currently
supports Turkish, English, German, French, Portuguese, Spanish,
Polish, Norwegian, Dutch, Italian.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_postacidir}/{classes,images,includes,lang,tmp/{send,store},queries/UPGRADE}

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{FAQ/FAQ,TODO,WHATSNEW,THANKS,INSTALL,UPGRADE}
%dir %{_postacidir}
# %attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_postacidir}/config.inc.php
%{_postacidir}/classes
%{_postacidir}/images
%{_postacidir}/includes
%{_postacidir}/lang
%{_postacidir}/queries
%{_postacidir}/*.php
%{_postacidir}/.htaccess
%{_postacidir}/INSTALL
