import os, argparse
#Creates Command line Argument Parsers
parser=argparse.ArgumentParser(usage='Quickly install or reinstall servers',description='Used to install 1 or more servers including: Apache 2.4, NFS, and LDAP  |  Format: python3 ./install-server [-l,--ldap][-n,--nfs][-a,--apache]',add_help=True,allow_abbrev=True)
parser.add_argument('-l','--ldap', help='installs and Configure LDAP services using openldap and its dependencies.',action='store_const', const='ldap')
parser.add_argument('-n','--nfs', help='installs and Configure NFS services',action='store_const', const='nfs')
parser.add_argument('-a','--apache', help='installs and Configure apache webserver 2.4 services using openldap and its dependencies.',action='store_const', const='apache')
args = parser.parse_args()

def ldap():
	# Installs software and Downloads files
	os.system('echo Installing LDAP and Configurations.... | tee  -a /var/log/ldap_install.log; yum install -y openldap-servers openldap-clients nss_ldap migrationtools >> /var/log/ldap_install.log 2>&1; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/olc2 https://github.com/NKU-2-4orBUST/Project2/raw/main/base.ldif https://github.com/NKU-2-4orBUST/Project2/raw/main/diradm.conf https://github.com/NKU-2-4orBUST/Project2/raw/main/migrate_common.ph http://www.hits.at/diradm/diradm-1.3.tar.gz  >> /var/log/ldap_install.log 2>&1')
	# Sets Configurations for LDAP server
	os.system('echo Configuring LDAP.... | tee  -a /var/log/ldap_install.log; cat /tmp/olc2 > /etc/openldap/slapd.d/cn\=config/olcDatabase\=\{2\}hdb.ldif | tee -a /var/log/ldap_install.log; cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG >> /var/log/ldap_install.log 2>&1; cat ./migrate_common.ph > /usr/share/migrationtools/migrate_common.ph | tee -a /var/log/ldap_install.log; cat ./base.ldif > /usr/share/migrationtools/base.ldif  | tee -a /var/log/ldap_install.log; tar -xvf diradm-1.3.tar.gz -C /usr/local >> /var/log/ldap_install.log 2>&1; cp /usr/local/diradm-1.3/diradm.conf /etc/ >> /var/log/ldap_install.log 2>&1; cat ./diradm.conf > /etc/diradm.conf | tee -a /var/log/ldap_install.log')
	# Migrates system user and groups to LDAP services and set the owner of all files in /var/lib/ldap as ldap
	os.system('echo Migrating Users and Groups to LDAP database.... | tee -a /var/log/ldap_install.log; systemctl start slapd  >> /var/log/ldap_install.log 2>&1; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/core.ldif | tee -a /var/log/ldap_install.log; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/cosine.ldif | tee -a /var/log/ldap_install.log; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/nis.ldif  | tee -a /var/log/ldap_install.log; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/inetorgperson.ldif | tee -a /var/log/ldap_install.log; systemctl stop slapd  >> /var/log/ldap_install.log 2>&1; chown -R ldap:ldap /var/lib/ldap  | tee -a /var/log/ldap_install.log; slapadd -v -l /usr/share/migrationtools/base.ldif  | tee -a /var/log/ldap_install.log; /usr/share/migrationtools/migrate_passwd.pl /etc/passwd > /usr/share/migrationtools/passwd.ldif | tee -a /var/log/ldap_install.log; slapadd -v -l /usr/share/migrationtools/passwd.ldif | tee -a /var/log/ldap_install.log; /usr/share/migrationtools/migrate_group.pl /etc/group > /usr/share/migrationtools/group.ldif  | tee -a /var/log/ldap_install.log; slapadd -v -l /usr/share/migrationtools/group.ldif  | tee -a /var/log/ldap_install.log; chown -R ldap:ldap /var/lib/ldap  | tee -a /var/log/ldap_install.log; systemctl start slapd >> /var/log/ldap_install.log 2>&1; systemctl -l status slapd >> /var/log/ldap_install.log 2>&1')
	# Configures Firewall for LDAP service
	os.system('echo Configuring firewall for LDAP services.... | tee -a /var/log/ldap_install.log; firewall-cmd --zone=public --add-port=389/tcp --permanent >> /var/log/ldap_install.log 2>&1; firewall-cmd --zone=public --add-port=636/tcp --permanent >> /var/log/ldap_install.log 2>&1; firewall-cmd --reload >> /var/log/ldap_install.log 2>&1; firewall-cmd --list-all  >> /var/log/ldap_install.log 2>&1')
def nfs():
	# Downloading configuration files and installing NFS  erase if no longer needed -- https://github.com/NKU-2-4orBUST/Project2/raw/main/fstab.txt
	os.system('yum install -y nfs-utils rpcbin; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/exports.txt; exportfs -a  ')
	# Exporting /HOME directory and starting NFS and required services
	os.system('cat exports.txt > /etc/exports; systemctl start nfs; systemctl start nfslock') 
	#Firewall configured and reloaded.
	os.system('firewall-cmd --zone=public --add-port=2049/tcp --permanent; firewall-cmd --zone=public --add-port=111/tcp --permanent; firewall-cmd --zone=public --add-port=20048/tcp --permanent; firewall-cmd --zone=public --add-port=2049/udp --permanent; firewall-cmd --zone=public --add-port=111/udp --permanent; firewall-cmd --zone=public --add-port=20048/udp --permanent; systemctl restart firewalld')

def apache():	
	#Downloads required Configs and Installs software
	os.system('echo Installing Apache 2.4 and Mod_ssl.... | tee  -a /var/log/apache_install.log; yum -y install httpd mod_ssl >> /var/log/apache_install.log 2>&1; wget https://github.com/NKU-2-4orBUST/Project1/raw/main/httpd.conf https://github.com/NKU-2-4orBUST/Project1/raw/main/userdir.conf >> /var/log/apache_install.log 2>&1')
	#Configures apache 2.4 web server
	os.system('echo Configuring Apache Webserver... | tee -a /var/log/apache_install.log; \\cp httpd.conf /etc/httpd/conf >> /var/log/apache_install.log; \\cp userdir.conf /etc/httpd/conf.d/ >> /var/log/apache_install.log; mkdir /etc/httpd/ssl') #Replaces apache config and userdir.conf with know good config
	#Changes to new SLL directory to generate SSL keys in the next step
	os.chdir('/etc/httpd/ssl')#Changes to SSL directory
	#Generates SSL keys for HTTPS 
	os.system('openssl genrsa -out 10_2_7_71_Group_2.key 1024 >> /var/log/apache_install.log 2>&1; openssl req -new -key 10_2_7_71_Group_2.key -subj "/C=US/ST=Kentucky/L=Highland Heights/O=NKU/CN=10-2-7-71-Group-2" -out 10_2_7_71_Group_2.csr; openssl x509 -req -days 365 -in 10_2_7_71_Group_2.csr -signkey 10_2_7_71_Group_2.key -out 10_2_7_71_Group_2.crt >> /var/log/ApacheInstallScriptLog 2>&1')# Creates .key file for SSL 
	#Configures the firewall and starts apache webserver
	os.system('echo Configuring Firewall for Apache | tee -a /var/log/apache_install.log; sudo firewall-cmd --permanent --add-port=80/tcp >> /var/log/apache_install.log 2>&1; sudo firewall-cmd --permanent --add-port=443/tcp >> /var/log/apache_install.log 2>&1; sudo firewall-cmd --reload>> /var/log/apache_install.log 2>&1; echo Waiting for Firewall to reload | tee  -a /var/log/apache_install.log; sleep 5; echo Firewall reloaded | tee  -a /var/log/apache_install.log; systemctl -l status firewalld >> /var/log/apache_install.log 2>&1; systemctl start httpd >> /var/log/apache_install.log 2>&1; systemctl status httpd >> /var/log/apache_install.log 2>&1 ') 
	#Configures system settings to allow public traffic.
	os.system('setsebool -P httpd_enable_homedirs on; chcon -R -t httpd_sys_content_t /home/; chcon -R -t httpd_sys_rw_content_t /home/')

def main(args):
	#Changes pythons to tmp directory save files just for the install
	os.chdir('/tmp')
    	#Starts LDAP Install
	if args.ldap == 'ldap':
		print('Installing LDAP ')
		ldap()
	#Starts NFS Install
	if args.nfs == 'nfs':
		print('Starting NFS')
		nfs()
	#Starts Apache Install
	if args.apache == 'apache':
		print('Installing Apache Web Server 2.4')
		apache()
	sys('echo "System will reboot in 5 seconds..."; shutdown -r 5')

main(args)
