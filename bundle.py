import os
import MySQLdb

#update IP here
depIP = '10.200.172.28'

with open('currVers.txt', 'r+') as f:
	vers = f.read()
	vers = int(vers)
	vers+= 1	
	f.seek(0)
	f.write(str(vers))
	f.truncate()

newDir = '../front_v' + str(vers)
bund = 'frontend_v' + str(vers) + '.zip '
remLoc = '/home/paul/deploy/bundles/' + bund

#zip up dir and create bundle
os.system('cp -r /var/www/somethingpatheticallyawful.com/public_html ' + newDir)
os.system('zip -r ' + bund + newDir)

#scp to deploy server
os.system('scp ' + bund + 'paul@' + depIP + ':/home/paul/deploy/bundles/')

#add index to remote DB
myDB = MySQLdb.connect(host=depIP,port=3306,user="dmz",passwd="letMe1n",db="user_info")
curs = myDB.cursor()
curs.execute("insert into bundles(name, location)  values('" + bund + "', '" + remLoc + "');")
myDB.commit()

#delete local copy of dir and bundle
os.system('sudo rm -r ' + newDir)
os.system('sudo rm -r ' + bund)

