# coding=utf-8
import docx
import os
import json
import codecs
import re
#import update_table

_POI = [u"ליקוי", u"מעקב"]
_INSPECTED = u"הגופים המבוקרים:"
_FISCAL_FIRST = 1948
_REGULAR_FIRST = 1950
EM_DASH = u"\u2013"

def get_ref(name, collection):
	for entry in collection:
		if entry["name"] == name:
			return entry["name"] #TODO: use slug instead of name
	else:
		collection.append( { "name": name, "slug": hash( name ) } )
		return collection[-1]["name"] #TODO: use slug instead of name
		
		
def _create_report( collection, id ):
	for report in collection:
		if report["slug"] == id:
			break
	else:
		report_id = re.match( "(\d+)([a-zA-Z])", id )
		fiscal = 1 if report_id.groups(0)[1] == "b" else 0
		year = int(report_id.groups(0)[0]) + _FISCAL_FIRST if fiscal else _REGULAR_FIRST
		collection.append( { "year": year, "fiscal": fiscal, "slug": id, "link": "" } )
		#TODO: add link to the Mevaker website
	
	return id
	

def _create_simple_object( collection, id ):
	for object in collection:
		if object["slug"] == hash(id):
			break
	else:
		collection.append( { "name": id, "slug": hash( id ) } )
	
	return collection[-1]["slug"]
	

def _parse_inspected( collection, raw_string):
	#TODO: Parse offices & bodies differently
	inspected = []
	raw_string = raw_string.replace( EM_DASH, u"-" ) #replace em-dash
	inspectees = raw_string.split( ":" )
	inspectees = inspectees[0].split( ";" ) if len(inspectees) == 1 else inspectees[1].split( ";" )
	for inspectee in inspectees:
		if inspectee.find( u"-" ) == -1:
			inspected.append( _create_simple_object( collection, inspectee.strip() ) )
			collection[-1]["parent"] = ""
		else:
			inspectee = inspectee.split( u"-" )
			inspected.append( _create_simple_object( collection, inspectee[1].strip() ) )
			collection[-2]["parent"] = _parse_inspected( collection, inspectee[0].strip() )[0]
			
	return inspected

	
def _save_issue( collection, ids, type, text, topic, report, inspected ):
	#print ids
	if type == 0: #Create new issue
		collection.append( { "id": int( ids[0] ), "text": text, "type": 0, "status": 3, "followups": [], "topic": topic, "report": report, "inspected": inspected, "slug": "%s/%s/%s" % ( report, topic, int( ids[0] ) ) } )
	elif type == 1: #Add followup text to an issue
		#TODO: Save per unit followups
		for id in ids:
			for issue in collection:
				if issue["id"] == int( id ):
					issue["followups"].append( text )
					if issue["status"] != 1:
						issue["status"] = 2
	
	
def main():
	os.chdir(os.path.dirname(__file__)) #Working path fix for NppExec, remove in production
	
	#Init data structures
	offices = [] #list of { name, parent = "", slug }
	topics = [] #list of { name, link = "", slug }
	reports = [] #list of { year, fiscal = 0, link = "", slug }
	issues = [] #list of { id, text, status, type = 0, followups = [], topic, report, inspected = [] }
	
	#Process reports data
	for report_dir in os.listdir( "./data" ):
		report = _create_report( reports, report_dir )
		for file in os.listdir( "./data/%s" % ( report_dir, ) ):
			print "./data/%s/%s" % (report, file)
			doc = [] #Issues in this doc
			count = 1
			
			#Get the document contents (text only, no structure)
			paragraphs = docx.getdocumenttext(docx.opendocx("./data/%s/%s" % (report, file)))
			
			#Get the header (everything above the inspected bodies)
			lead = []
			for p in paragraphs:
				if _INSPECTED in p:
					inspected = _parse_inspected( offices, p )
					paragraphs.remove( p )
					break
				
				lead.append( p )
				
			paragraphs = [p for p in paragraphs if p not in lead] #Filter paragraphs
			topic = _create_simple_object( topics, lead[-1] ) #Get the topic slug
			
			#Flags
			off_by_one = True
			poi_text = False 
			
			for p in paragraphs: #Handle the document body
				#print p.encode("utf-8")
				p = p.strip()
				if off_by_one: #Log fixed issues
					prev = -1
					for issue_id in re.findall( "(\d+)", p ):
						if prev == -1 or p.index( issue_id ) <= prev + 4:
							_save_issue(doc, [issue_id], 0, "", topic, report, inspected)
							doc[-1]["status"] = 1
							prev = p.index( issue_id )
					
					off_by_one = False
				else: #Extract issue/followup text
					if p in _POI:
						#print "poi"
						#Save old issue
						if poi_text:
							_save_issue(doc, ids, type, text, topic, report, inspected)
							
						poi_text = True
						type = _POI.index( p )
						ids = []
					elif poi_text:
						#print "poi text"
						if len(ids) == 0: #get ids range
							new_id = re.match( "(\d+.?)", p )
							if new_id is None:
								ids = [count]
								text = p
							else:
								new_id = p[0:p.find( "." )] #Handle only the suspected ids
								new_id.replace( EM_DASH, "-" ) #Replace the em-dash
								new_id.replace( u" ", "" ) #Remove whitespace
								ids = new_id.split( "," )
								if len(ids) == 1:
									ids = ids[0].split( "-" )
									if len(ids) == 2:
										ids = range( int( ids[0] ), int( ids[1] ) + 1 )
										
								if len(ids) == 0:
									ids = [count]
								
								count += 1
								text = p[p.find( "." ) + 1:]
						else:
							text += p
			
			_save_issue(doc, ids, type, text, topic, report, inspected)
			issues.extend( doc )
			
	#Serialize results
	json.dump( offices, open( "./offices.json", "w+" ) )
	json.dump( reports, open( "./reports.json", "w+" ) )
	json.dump( topics, open( "./topics.json", "w+" ) )
	json.dump( issues, open( "./issues.json", "w+" ) )

if __name__ == "__main__":
	main()
