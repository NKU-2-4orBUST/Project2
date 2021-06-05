import os, argparse
#Creates Command line Argument Parsers
parser=argparse.ArgumentParser(usage='Quickly install or reinstall servers',description='Used to install 1 or more servers including: Apache 2.4, NFS, and LDAP  |  Format: python3 ./install-server [-l,--ldap][-n,--nfs][-a,--apache]',add_help=True,allow_abbrev=True)
parser.add_argument('-l','--ldap', help='installs and Configure LDAP services using openldap and its dependencies.',action='store_const', const='ldap')
parser.add_argument('-n','--nfs', help='installs and Configure NFS services',action='store_const', const='nfs')
parser.add_argument('-a','--apache', help='installs and Configure apache webserver 2.4 services using openldap and its dependencies.',action='store_const', const='apache')
args = parser.parse_args()

def ldap():
	#os.system('yum -y install openldap-servers openldap-clients  >> /var/log/ldap.log; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/olc2 http://faculty.cs.nku.edu/~waldenj/classes/2011/summer/cit470/labs/example.ldif')
	#os.system('rm -f /var/lib/ldap/*  >> /var/log/ldap.log; cat ./olc2 > /etc/openldap/slapd.d/cn=config/olcDatabase={2}hdb.ldif  | tee /var/log/ldap.log')
	#os.system('ldapadd -x -D "cn=Manager,dc=cit470,dc=nku,dc=edu" -w Nhy67ujm! -f example.ldif  | tee /var/log/ldap')
	#os.system('firewall-cmd --zone=public --add-port=389/tcp --permanent  >> /var/log/ldap.log; firewall-cmd --zone=public --add-port=636/tcp --permanent  >> /var/log/ldap.log; systemctl restart firewalld  >> /var/log/ldap.log >> systemctl status firewalld  >> /var/log/ldap.log')
	#os.system('systemctl start slapd, systemctl status slapd')	
	
	#Installs software and Downloads files
	os.system('yum install -y openldap-servers openldap-clients nss_ldap migrationtools; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/olc2 http://faculty.cs.nku.edu/~waldenj/classes/2011/summer/cit470/labs/example.ldif https://github.com/NKU-2-4orBUST/Project2/raw/main/olc2 https://github.com/NKU-2-4orBUST/Project2/raw/main/base.ldif https://github.com/NKU-2-4orBUST/Project2/raw/main/diradm.conf https://github.com/NKU-2-4orBUST/Project2/raw/main/migrate_common.ph http://www.hits.at/diradm/diradm-1.3.tar.gz')
	#Sets Configurations for LDAP server
	os.system('cat /root/olc2 > /etc/openldap/slapd.d/cn=config/olcDatabase={2}hdb.ldif; rm /var/lib/ldap/*; cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG; cat ./migrate_common.ph > /usr/share/migrationtools/migrate_common.ph; cat ./base.ldif > /usr/share/migrationtools/base.ldif; tar -xvf diradm-1.3.tar.gz -C /usr/local; cp /usr/local/diradm-1.3/diradm.conf /etc/; cat ./diradm.conf > /etc/diradm.conf')
	#os.system('ldapadd -x -D "cn=Manager,dc=cit470,dc=nku,dc=edu" -w Nhy67ujm! -f example.ldif')
	#Migrates system user and groups to LDAP services and set the owner of all files in /var/lib/ldap as ldap
	os.system('systemctl start slapd; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/core.ldif; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/cosine.ldif; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/nis.ldif; ldapadd -Y EXTERNAL -H ldapi:// -f /etc/openldap/schema/inetorgperson.ldif; systemctl stop slapd; chown -R ldap:ldap /var/lib/ldap; slapadd -v -l /usr/share/migrationtools/base.ldif; /usr/share/migrationtools/migrate_passwd.pl /etc/passwd > /usr/share/migrationtools/passwd.ldif; slapadd -v -l /usr/share/migrationtools/passwd.ldif; /usr/share/migrationtools/migrate_group.pl /etc/group > /usr/share/migrationtools/group.ldif; chown -R ldap:ldap /var/lib/ldap; systemctl start slapd; systemctl -l status slapd')
	#Configures Firewall for LDAP service
	os.system('firewall-cmd --zone=public --add-port=389/tcp --permanent; firewall-cmd --zone=public --add-port=636/tcp --permanent; firewall-cmd --reload')
def nfs():
	#Downloading configuration files and installing NFS
	os.system ('yum install -y nfs-utils; wget https://github.com/NKU-2-4orBUST/Project2/raw/main/fstab https://github.com/NKU-2-4orBUST/Project2/raw/main/exports; exportfs -a  ')
	# and mounting new partition
	os.system('systemctl start nfs; systemctl start nfslock; systemctl start rpcbin') # starting NFS and required services
	#Firewall configured and reloaded.
	os.system ('firewall-cmd --zone=public --add-port=2049/tcp --permanent; firewall-cmd --zone=public --add-port=111/tcp --permanent; firewall-cmd --zone=public --add-port=20048/tcp --permanent; firewall-cmd --zone=public --add-port=2049/udp --permanent; firewall-cmd --zone=public --add-port=111/udp --permanent; firewall-cmd --zone=public --add-port=20048/udp --permanent; systemctl restart firewalld')

def apache():
	#Changes pythons to tmp directory save files just for the install
	os.chdir('/tmp')	
	#Downloads required Configs and Installs software
	os.system('echo Installing Apache 2.4 and Mod_ssl.... | tee  -a /root/apache_install.log; yum -y install httpd mod_ssl >> /root/apache_install.log 2>&1; wget https://github.com/NKU-2-4orBUST/Project1/raw/main/httpd.conf https://github.com/NKU-2-4orBUST/Project1/raw/main/userdir.conf >> /root/apache_install.log 2>&1')
	#Configures apache 2.4 web server
	os.system('echo Configuring Apache Webserver... | tee -a /root/apache_install.log; \\cp httpd.conf /etc/httpd/conf >> /root/apache_install.log; \\cp userdir.conf /etc/httpd/conf.d/ >> /root/apache_install.log; mkdir /etc/httpd/ssl') #Replaces apache config and userdir.conf with know good config
	#Changes to new SLL directory to generate SSL keys in the next step
	os.chdir('/etc/httpd/ssl')#Changes to SSL directory
	#Generates SSL keys for HTTPS 
	os.system('openssl genrsa -out 10_2_7_71_Group_2.key 1024 >> /root/apache_install.log 2>&1; openssl req -new -key 10_2_7_71_Group_2.key -subj "/C=US/ST=Kentucky/L=Highland Heights/O=NKU/CN=10-2-7-71-Group-2" -out 10_2_7_71_Group_2.csr; openssl x509 -req -days 365 -in 10_2_7_71_Group_2.csr -signkey 10_2_7_71_Group_2.key -out 10_2_7_71_Group_2.crt >> /root/ApacheInstallScriptLog 2>&1')# Creates .key file for SSL 
	#Configures the firewall and starts apache webserver
	os.system('echo Configuring Firewall for Apache | tee -a /root/apache_install.log; sudo firewall-cmd --permanent --add-port=80/tcp >> /root/apache_install.log 2>&1; sudo firewall-cmd --permanent --add-port=443/tcp >> /root/apache_install.log 2>&1; sudo firewall-cmd --reload>> /root/apache_install.log 2>&1; echo Waiting for Firewall to reload | tee  -a /root/apache_install.log; sleep 5; echo Firewall reloaded | tee  -a /root/apache_install.log; systemctl -l status firewalld >> /root/apache_install.log 2>&1; systemctl start httpd >> /root/apache_install.log 2>&1; systemctl status httpd >> /root/apache_install.log 2>&1 ') 
	#Configures system settings to allow public traffic.
	os.system('setsebool -P httpd_enable_homedirs on; chcon -R -t httpd_sys_content_t /home/; chcon -R -t httpd_sys_rw_content_t /home/')

def main(args):
    	#Starts LDAP Install
    	if args.ldap == 'ldap': 
        	print('Starting ldap install')
        	ldap()
	#Starts NFS Install
    	if args.nfs == 'nfs': 
        	print('Starting NFS')
        	nfs()
	#Starts Apache Install
    	if args.apache == 'apache': # Starts Apache Install
        	print('Future space for apache web server: PENDING APPROVAL')
        	apache()

main(args)
