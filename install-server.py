import os, argparse
#Creates Command line Argument Parsers
parser=argparse.ArgumentParser(usage='Quickly install or reinstall servers',description='Used to install 1 or more servers including: Apache 2.4, NFS, and LDAP  |  Format: python3 ./install-server [-l,--ldap][-n,--nfs][-a,--apache]',add_help=True,allow_abbrev=True)
parser.add_argument('-l','--ldap', help='installs and Configure LDAP services using openldap and its dependencies.',action='store_const', const='ldap')
parser.add_argument('-n','--nfs', help='installs and Configure NFS services',action='store_const', const='nfs')
parser.add_argument('-a','--apache', help='installs and Configure apache webserver 2.4 services using openldap and its dependencies.',action='store_const', const='apache')
args = parser.parse_args()

def ldap(): # Function to Install LDAP
	# Installs software and Downloads files
	os.system('echo Installing LDAP and Downloading LDAP Configuration files.... | tee  -a /var/log/ldap_install.log; yum install -y openldap-servers openldap-clients nss_ldap migrationtools >> /var/log/ldap_install.log 2>&1; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/olc2 https://github.com/NKU-2-4orBUST/Project2/raw/main/base.ldif https://github.com/NKU-2-4orBUST/Project2/raw/main/diradm.conf https://github.com/NKU-2-4orBUST/Project2/raw/main/migrate_common.ph http://www.hits.at/diradm/diradm-1.3.tar.gz  >> /var/log/ldap_install.log 2>&1')
	# Sets Configurations for LDAP server
	os.system('echo Configuring LDAP.... | tee  -a /var/log/ldap_install.log;cat /tmp/olc2 > /etc/openldap/slapd.d/cn\=config/olcDatabase\=\{2\}hdb.ldif; rm /var/lib/ldap/* >> /var/log/ldap_install.log 2>&1; cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG >> /var/log/ldap_install.log 2>&1; cat ./migrate_common.ph > /usr/share/migrationtools/migrate_common.ph; cat ./base.ldif > /usr/share/migrationtools/base.ldif; tar -xvf diradm-1.3.tar.gz -C /usr/local >> /var/log/ldap_install.log 2>&1; cp /usr/local/diradm-1.3/diradm.conf /etc/ >> /var/log/ldap_install.log 2>&1; cat ./diradm.conf > /etc/diradm.conf')
	# Migrates system user and groups to LDAP services and set the owner of all files in /var/lib/ldap as ldap
	os.system('echo Migrating Users and Groups into LDAP database.... | tee  -a /var/log/ldap_install.log; systemctl start slapd >> /var/log/ldap_install.log 2>&1; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/core.ldif >> /var/log/ldap_install.log 2>&1; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/cosine.ldif >> /var/log/ldap_install.log 2>&1; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/nis.ldif >> /var/log/ldap_install.log 2>&1; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/inetorgperson.ldif >> /var/log/ldap_install.log 2>&1; systemctl stop slapd >> /var/log/ldap_install.log 2>&1; chown -R ldap:ldap /var/lib/ldap >> /var/log/ldap_install.log 2>&1; slapadd -v -l /usr/share/migrationtools/base.ldif >> /var/log/ldap_install.log 2>&1; /usr/share/migrationtools/migrate_passwd.pl /etc/passwd > /usr/share/migrationtools/passwd.ldif >> /var/log/ldap_install.log 2>&1; slapadd -v -l /usr/share/migrationtools/passwd.ldif >> /var/log/ldap_install.log 2>&1; /usr/share/migrationtools/migrate_group.pl /etc/group > /usr/share/migrationtools/group.ldif  >> /var/log/ldap_install.log 2>&1; slapadd -v -l /usr/share/migrationtools/group.ldif >> /var/log/ldap_install.log 2>&1; chown -R ldap:ldap /var/lib/ldap >> /var/log/ldap_install.log 2>&1; systemctl start slapd >> /var/log/ldap_install.log 2>&1; systemctl enable slapd >> /var/log/ldap_install.log 2>&1; systemctl -l status slapd >> /var/log/ldap_install.log 2>&1')
	# Configures Firewall for LDAP service
	os.system('echo Configuring Firewall for LDAP.... | tee  -a /var/log/ldap_install.log; firewall-cmd --zone=public --add-port=389/tcp --permanent  >> /var/log/ldap_install.log 2>&1; firewall-cmd --zone=public --add-port=636/tcp --permanent >> /var/log/ldap_install.log 2>&1; systemctl restart firewalld >> /var/log/ldap_install.log 2>&1; sleep 5; firewall-cmd --list-all >> /var/log/ldap_install.log 2>&1')

def nfs(): # Function to Install NFS
	# Downloading configuration files and installing NFS  erase if no longer needed -- https://github.com/NKU-2-4orBUST/Project2/raw/main/fstab.txt
	os.system('echo Installing NSF and Downloading NFS Configuration files.... | tee  -a /var/log/nfs_install.log; yum install -y nfs-utils rpcbin >> /var/log/nfs _install.log 2>&1; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/exports.txt  >> /var/log/nfs _install.log 2>&1; exportfs -a  >> /var/log/nfs _install.log 2>&1')
	# Exporting /HOME directory and starting NFS and required services
	os.system('echo Exporting /HOME directory and starting NFS and required services.... | tee  -a /var/log/nfs_install.log; cat exports.txt > /etc/exports; systemctl start nfs  >> /var/log/nfs _install.log 2>&1; systemctl start nfslock >> /var/log/nfs _install.log 2>&1; systemctl enable slapd >> /var/log/nfs_install.log 2>&1; systemctl status nfs nfslock  >> /var/log/nfs _install.log 2>&1') 
	# Firewall configured and reloaded.
	os.system('echo Configuring Firewall for NFS.... | tee  -a /var/log/nfs_install.log; firewall-cmd --zone=public --add-port=2049/tcp --permanent  >> /var/log/nfs _install.log 2>&1; firewall-cmd --zone=public --add-port=111/tcp --permanent >> /var/log/nfs _install.log 2>&1; firewall-cmd --zone=public --add-port=20048/tcp --permanent >> /var/log/nfs _install.log 2>&1; firewall-cmd --zone=public --add-port=2049/udp --permanent >> /var/log/nfs _install.log 2>&1; firewall-cmd --zone=public --add-port=111/udp --permanent >> /var/log/nfs _install.log 2>&1; firewall-cmd --zone=public --add-port=20048/udp --permanent >> /var/log/nfs _install.log 2>&1; echo Restarting Firewall.... | tee  -a /var/log/nfs_install.log; systemctl restart firewalld >> /var/log/nfs _install.log 2>&1; sleep 5; firewall-cmd --list-all >> /var/log/nfs _install.log 2>&1')

def apache(): # Function to Install Apache Web Server 2.4	
	# Downloads required Configs and Installs software
	os.system('echo Installing Apache 2.4 and Mod_ssl.... | tee  -a /var/log/apache_install.log; yum -y install httpd mod_ssl >> /var/log/apache_install.log 2>&1; wget https://github.com/NKU-2-4orBUST/Project1/raw/main/httpd.conf https://github.com/NKU-2-4orBUST/Project1/raw/main/userdir.conf >> /var/log/apache_install.log 2>&1')
	# Configures apache 2.4 web server
	os.system('echo Configuring Apache Webserver... | tee -a /var/log/apache_install.log; \\cp httpd.conf /etc/httpd/conf >> /var/log/apache_install.log; \\cp userdir.conf /etc/httpd/conf.d/ >> /var/log/apache_install.log; mkdir /etc/httpd/ssl') #Replaces apache config and userdir.conf with know good config
	# Changes to new SLL directory to generate SSL keys in the next step
	os.chdir('/etc/httpd/ssl')#Changes to SSL directory
	# Generates SSL keys for HTTPS 
	os.system('openssl genrsa -out 10_2_7_71_Group_2.key 1024 >> /var/log/apache_install.log 2>&1; openssl req -new -key 10_2_7_71_Group_2.key -subj "/C=US/ST=Kentucky/L=Highland Heights/O=NKU/CN=10-2-7-71-Group-2" -out 10_2_7_71_Group_2.csr; openssl x509 -req -days 365 -in 10_2_7_71_Group_2.csr -signkey 10_2_7_71_Group_2.key -out 10_2_7_71_Group_2.crt >> /var/log/ApacheInstallScriptLog 2>&1')# Creates .key file for SSL 
	#Configures the firewall and starts apache webserver
	os.system('echo Configuring Firewall for Apache | tee -a /var/log/apache_install.log; sudo firewall-cmd --permanent --add-port=80/tcp >> /var/log/apache_install.log 2>&1; sudo firewall-cmd --permanent --add-port=443/tcp >> /var/log/apache_install.log 2>&1; sudo firewall-cmd --reload>> /var/log/apache_install.log 2>&1; echo Waiting for Firewall to reload | tee  -a /var/log/apache_install.log; sleep 5; echo Firewall reloaded | tee  -a /var/log/apache_install.log; firewall-cmd --list-all >> /var/log/apache_install.log 2>&1; systemctl start httpd >> /var/log/apache_install.log 2>&1; systemctl enable httpd >> /var/log/apache_install.log 2>&1; systemctl status httpd >> /var/log/apache_install.log 2>&1') 
	#Configures system settings to allow public traffic.
	os.system('setsebool -P httpd_enable_homedirs on >> /var/log/apache_install.log 2>&1; chcon -R -t httpd_sys_content_t /home/ >> /var/log/apache_install.log 2>&1; chcon -R -t httpd_sys_rw_content_t /home/ >> /var/log/apache_install.log 2>&1')

def main(args):
	# Changes pythons to tmp directory save files just for the install
	os.chdir('/tmp')
    	# Starts LDAP Install
	if args.ldap == 'ldap':
		ldap()
		os.system('echo LDAP Installed! | tee -a /var/log/apache_install.log; sleep 5')
	#Starts NFS Install
	if args.nfs == 'nfs':
		nfs()
		os.system('echo NFS Installed! | tee -a /var/log/apache_install.log; sleep 5')
	#Starts Apache Install
	if args.apache == 'apache':
		apache()
		os.system('echo Apache Web Server 2.4 Installed! | tee -a /var/log/apache_install.log; sleep 5')
	if args.apache == 'apache' or args.nfs == 'nfs' or args.ldap == 'ldap':
		os.sys('echo "System will reboot in 5 seconds..."; shutdown -r 5')

main(args)
