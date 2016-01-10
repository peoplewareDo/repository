buildarch="$(uname -m)"

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat-native/SPECS/ulyaoth-tomcat-native1.2.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-tomcat-native1.2.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-tomcat-native1.2.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-tomcat-native1.2.spec
fi

su ulyaoth -c "spectool ulyaoth-tomcat-native1.2.spec -g -R"

if [ grep -q -i "release 19" /etc/fedora-release ] || [ grep -q -i "release 20" /etc/fedora-release ] || [ grep -q -i "release 21" /etc/fedora-release ] || [ grep -q -i "release 22" /etc/fedora-release ]
then
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
elif [ grep -q -i "release 6" /etc/redhat-release ] || [ grep -q -i "release 7" /etc/redhat-release ]
then
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
else
su ulyaoth -c "rpmbuild -ba ulyaoth-tomcat-native1.2.spec"
fi




cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-ulyaoth-tomcat-native1.2.sh