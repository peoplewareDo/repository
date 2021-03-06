
%define tomcat_group tomcat
%define tomcat_user tomcat

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    Tomcat multiple instances
Name:       ulyaoth-tomcat-multi
Version:    1.0.2
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://www.ulyaoth.net
Vendor:     Ulyaoth
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/functions
Source1:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/preamble
Source2:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/server
Source3:	https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/tomcat@.service
Source4:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-multi/SOURCES/tomcat-multi
BuildRoot:  %{_tmppath}/tomcat-multi-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{use_systemd}
Requires: ulyaoth-jsvc
%endif

Provides: ulyaoth-tomcat-multi
Provides: tomcat-multi

%description
This module adds all the scripts to a server so you can use a ulyaoth tomcat installation with multiple instances.
This rpm is based on the scripts that Fedora 23 provides for their tomcat but changed to fit ulyaoth tomcat.


%prep

%build

%install
%{__mkdir} -p $RPM_BUILD_ROOT/usr/libexec/tomcat
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/tomcats
%{__mkdir} -p $RPM_BUILD_ROOT/usr/bin

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m 644 -p %{SOURCE0} \
   $RPM_BUILD_ROOT/usr/libexec/tomcat/functions
%{__install} -m 755 -p %{SOURCE1} \
   $RPM_BUILD_ROOT/usr/libexec/tomcat/preamble
%{__install} -m 755 -p %{SOURCE2} \
   $RPM_BUILD_ROOT/usr/libexec/tomcat/server
%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%{_unitdir}/tomcat@.service
%endif

 %{__install} -m755 %SOURCE4 \
        $RPM_BUILD_ROOT/usr/bin/tomcat-multi 
 
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /var/lib/tomcats
/usr/bin/tomcat-multi

%if %{use_systemd}
%{_unitdir}/tomcat@.service
/usr/libexec/tomcat/functions
/usr/libexec/tomcat/preamble
/usr/libexec/tomcat/server
%endif

%post
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-tomcat-multi!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

Please find the documentation for using tomcat multiple instances here:
* https://www.ulyaoth.net/threads/how-to-configure-multiple-tomcat-instances.82312/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Mon Mar 14 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.2-1
- Fixed tomcat-multi script so it does a correct exit 0 instead of exit 1.

* Sun Feb 21 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.2-1
- Fixed tomcat-multi script to not do the create part two times.

* Sun Dec 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.0.0-1
- Initial release.