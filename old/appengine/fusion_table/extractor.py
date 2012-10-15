# coding=utf-8
import docx
import os
import json
import codecs
import re
import update_table

_POI = [u"ליקוי", u"מעקב"]
_POI_TYPES = {0: "text", 1: "followup"}

def get_ref(name, collection):
	for entry in collection:
		if entry["name"] == name:
			return entry["name"] #TODO: use slug instead of name
	else:
		collection.append( { "name": name, "slug": hash( name ) } )
		return collection[-1]["name"] #TODO: use slug instead of name

def main():
	reports = os.listdir( "./data" )
	offices = []
	topics = []
	units = []
	#import pdb
	#pdb.set_trace()
	for report in reports:
		files = os.listdir( "./data/%s" % ( report, ) )
		for file in files:
			print "./data/%s/%s" % (report, file)
			paragraphs = docx.getdocumenttext(docx.opendocx("./data/%s/%s" % (report, file)))
			results = []
			flag = False
			type = -1 #type uninitialized
			
			office_name = get_ref( paragraphs[0].strip(), offices ) #First paragraph is the office
			topic = get_ref( paragraphs[1].strip(), topics ) #Second paragraph is the report topic
			
			#Third paragraph is the inspected units
			#TODO: More intelligent unit extraction
			if u"הגופים המבוקרים:" in paragraphs[2]:
				inspected = paragraphs[2].split(":")[1].strip().split(";")
				new_inspected = []
				for inspectee in inspected:
					inspectee = inspectee.replace(u"\u2014","-").split("-")
					inspectee = [i.strip() for i in inspectee]
					inspectee_name = inspectee[0] if len(inspectee) == 1 else inspectee[1]
					unit = filter( lambda x: x["name"] == inspectee_name, units)
					if len( unit ) == 0:
						office = "" if len( inspectee ) == 1 else get_ref( inspectee[0].strip(), offices )
						units.append( { "name": inspectee_name, "slug": hash( inspectee_name ), "office": office } )
						new_inspected.append( units[-1]["name"] ) #TODO: use slug instead of name
					else:
						new_inspected.append( unit[0]["name"] ) #TODO: use slug instead of name
			
			for paragraph in paragraphs:
				paragraph = paragraph.strip()
				if paragraph in _POI:
					flag = True
					results.append( { "id": 0, "type": 0, "status": 0, "text": "", "followup": "", "link": "", "report": report, "unit": "", "topic": topic.encode("utf-8"), "office": office_name.encode("utf-8") } )
					type = _POI.index(paragraph)
				elif flag:
					if re.match("(\d+)\.?", paragraph):
						results[-1]["id"] = int(re.match("(\d+)\.?", paragraph).groups(1)[0])
					
					results[-1][_POI_TYPES[type]] += re.sub("(\d+)\.?", "", paragraph).encode("utf-8") if len(paragraph) > 1 else ""
			
			#TODO: Properly compute status
			json.dumps(results, open("./results.json", "w+"))
			#A naive method to push the data to Google Fusion Table
			#for entry in results:
			#	for inspectee in new_inspected:
			#		update_table.insert_row( (entry["id"], entry["type"], entry["status"], entry["text"], entry["followup"], entry["link"], entry["report"], inspectee.encode("utf-8"), entry["topic"], entry["office"]) )
		

if __name__ == "__main__":
	main()