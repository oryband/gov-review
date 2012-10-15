'''
Created on Jun 04, 2011

@author: Drag0nR3b0rn
'''

from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL
import ftclient
from fileimport.fileimporter import CSVImporter

_TID = 946168

def insert_row( data ):
	token = ClientLogin().authorize(username, password)
	ft_client = ftclient.ClientLoginFTClient(token)
	
	query = "INSERT INTO 946168 (id, type, status, text, followup, link, report, unit, topic, office) VALUES (%d, %d, %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
	print query % data
	ft_client.query(query % data)