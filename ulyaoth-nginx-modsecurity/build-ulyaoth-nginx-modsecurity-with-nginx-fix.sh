ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 7" /etc/oracle-release
then
yum install -y http://mirror.centos.org/centos/7/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm
else
echo yeah Fedora!
fi

if type dnf 2>/dev/null
then
  dnf install -y pcre pcre-devel libxml2 libxml2-devel curl curl-devel httpd-devel yajl-devel lua-devel lua-static ssdeep-devel
elif type yum 2>/dev/null
then
  if grep -q -i "release 19" /etc/fedora-release || grep -q -i "release 20" /etc/fedora-release
  then
    yum install -y pcre pcre-devel libxml2 libxml2-devel curl curl-devel httpd-devel yajl-devel lua-devel lua-static
  elif grep -q -i "amazon" /etc/ulyaoth
  then
   yum install -y pcre pcre-devel libxml2 libxml2-devel curl curl-devel httpd-devel lua-devel lua-static
  else
    yum install -y pcre pcre-devel libxml2 libxml2-devel curl curl-devel httpd-devel yajl-devel lua-devel lua-static ssdeep-devel
  fi
fi

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
mkdir -p /etc/nginx/modules
cd /etc/nginx/modules
git clone -b nginx_refactoring https://github.com/SpiderLabs/ModSecurity.git modsecurity
cd modsecurity
./autogen.sh
./configure --enable-standalone-module
make
cd /etc/nginx/modules
tar cvf modsecurity.tar.gz modsecurity
mv modsecurity.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /etc/nginx/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modsecurity/SPECS/ulyaoth-nginx-modsecurity.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-modsecurity.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-modsecurity.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-modsecurity.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-modsecurity.spec -g -R"
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -bb ulyaoth-nginx-modsecurity.spec"
rm -rf /home/ulyaoth/rpmbuild/BUILD/*
rm -rf /home/ulyaoth/rpmbuild/BUILDROOT/*
rm -rf /home/ulyaoth/rpmbuild/RPMS/*
rm -rf /home/ulyaoth/rpmbuild/SOURCES/modsecurity.tar.gz
cd /etc/nginx/modules
tar cvf modsecurity.tar.gz modsecurity
mv modsecurity.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-nginx-modsecurity.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /home/ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild
