AutoReqProv: no
%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ulyaoth-openssl0.9.8
Version:    0.9.8zh
Release:    3%{?dist}
BuildArch: x86_64
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
%if 0%{?fedora}  == 19
Source0:    http://www.openssl.org/source/openssl-%{version}.tar.gz
%else
Source0:    https://www.openssl.org/source/openssl-%{version}.tar.gz
%endif
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SOURCES/ulyaoth-openssl0.9.8.conf
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: ulyaoth-openssl0.9.8
Provides: ulyaoth-openssl0.9.8zh

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%prep
%setup -q -n openssl-%{version}

%build
./config -Wl,-rpath=/usr/local/ulyaoth/ssl/openssl0.9.8/lib --openssldir=/usr/local/ulyaoth/ssl/openssl0.9.8 no-ssl2 no-ssl3 shared
make depend
make all
make rehash
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/local/ulyaoth/ssl/openssl0.9.8

make INSTALL_PREFIX=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-openssl0.9.8.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/ssl
%dir /usr/local/ulyaoth/ssl/openssl0.9.8
/usr/local/ulyaoth/ssl/openssl0.9.8/*
/etc/ld.so.conf.d/ulyaoth-openssl0.9.8.conf

%post -p /sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-openssl0.9.8!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%postun -p /sbin/ldconfig

%changelog
* Mon Oct 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-3
- Added ldd fixes.

* Mon Jan 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-2
- added "shared" to compile options.

* Sun Jan 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 0.9.8zh-1
- Initial release with openssl 0.9.8zh.