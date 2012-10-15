import json, sys, getpass, os, urllib, traceback, re
from fusion_table.authorization.clientlogin import ClientLogin
from fusion_table.sql.sqlbuilder import SQL
import fusion_table.ftclient as ftclient

_TID = 946168

def _find_slug( collection, slug ):
	for object in collection:
		if object["slug"] == slug:
			return object

def main():
	#os.chdir(os.path.dirname(__file__)) #Working path fix for NppExec, remove in production
	#Create Fusion Tables connection
	username = sys.argv[1]
	password = getpass.getpass("Enter your password: ")

	token = ClientLogin().authorize(username, password)
	ft_client = ftclient.ClientLoginFTClient(token)

	#Load data
	offices = json.load( open( "./offices.json", "r" ) )
	reports = json.load( open( "./reports.json", "r" ) )
	topics = json.load( open( "./topics.json", "r" ) )
	issues = json.load( open( "./issues.json", "r" ) )
	
	#Denormalize data
	flat_records = []
	i = 1
	for issue in issues:
		issue["topic"] = _find_slug( topics, issue["topic"] )["name"].encode("utf-8").replace("'", r"\'")
		issue["text"] = issue["text"].encode("utf-8").replace("'", r"\'")
		inspected = issue["inspected"]
		del issue["inspected"]
		followups = issue["followups"]
		del issue["followups"]
		issue["slug"] = issue["slug"].encode("utf-8").replace("'", r"\'")
		issue["report"] = issue["report"].encode("utf-8").replace("'", r"\'")
		issue["link"] = ""
		for followup in followups:
			issue["followup"] = followup.encode("utf-8").replace("'", r"\'")
			for inspectee in inspected:
				inspectee = _find_slug( offices, inspectee)
				if inspectee["parent"] == "":
					issue["unit"] = inspectee["name"].encode("utf-8").replace("'", r"\'")
					issue["office"] = inspectee["name"].encode("utf-8").replace("'", r"\'")
				else:
					issue["unit"] = inspectee["name"].encode("utf-8").replace("'", r"\'")
					issue["office"] = _find_slug( offices, inspectee["parent"])["name"].encode("utf-8").replace("'", r"\'")
					
				issue["id"] = i
				i += 1
				flat_records.append( issue )
	
	#Load data to the Fusion Table
	for record in flat_records:
		query = "INSERT INTO 946168 (id, type, status, text, followup, link, report, unit, topic, office, slug) VALUES (%d, %d, %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (record["id"], record["type"], record["status"], record["text"], record["followup"], record["link"], record["report"], record["unit"], record["topic"], record["office"], record["slug"])
		ft_client.query(query)

if __name__ == "__main__":
	main()