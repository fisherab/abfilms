#!/usr/bin/env python

import MySQLdb as mdb
import sys
import re
import datetime

def abort(msg):
    print >> sys.stderr, msg
    sys.exit(1)

args = sys.argv[1:]
if len(args) != 1: abort("Must have one argument")
password = args[0]

username = 'root'
schemain = 't'
schemaout = 'smf'
dbhost = 'localhost'

months =  ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

conin = mdb.connect(dbhost, username, password, schemain)
cur = conin.cursor()
conout = mdb.connect(dbhost, username, password, schemaout)

count = cur.execute("select p.post_title, p.post_name, p.post_date, p.post_content, t.name from wp_posts p, wp_term_relationships r, wp_term_taxonomy x, wp_terms t where x.term_id = t.term_id and r.term_taxonomy_id = x.term_taxonomy_id and r.object_id = p.id and post_status = 'publish' and post_type='post' order by p.post_title")


listings = {}
comments= {}
programmes = {}
titpat = re.compile(r"(.*)\((.*)\)")

def getTitle(title):            
    ftitle = None
    m = titpat.match(title)                                                                                
    if m: title, ftitle = m.groups()
    return title, ftitle
             
posts = cur.fetchall()
for post in posts:
    title, name, date, content, category = post
    if category in ["Newletters", "News items"]:
        pass
#        print title, name, category
    else:
        if "Listing" in category or "Screening" in category:
            category = "Listing"
        elif "Comments" in category:
            category = "Comments"
        elif "Programme" in category:
            category = "Programme"
        else:
            print "Odd category", category

        for s in ["SPECIAL EVENT","SILENT CLASSIC", "ADDITIONAL EVENT","THE ABCD SILENT CLASSIC","FREE SHOW","TH\
E ABCD ANNUAL SILENT CLASSIC"]:
            if title.startswith(s): title = title[len(s):].strip()
            if title.startswith("-"): title=title[1:].strip()

        if category == "Listing":
            bits = title.split(" - ")
            if len(bits) == 2:
                title, ftitle = getTitle(bits[0].strip())
                
                datestring = bits[1].strip()
                datebits = datestring.split()
                if len(datebits) == 2:
                    month, day = datebits
                    if month == "April": month = "Apr"
                    if month == "June": month = "Jun"
                    if month == "DEC": month = "Dec"
                    if month == "Sept": month = "Sep"
                    if month == "March": month = "Mar"
                    if month == "OCT": month = "Oct"
                    if month == "February": month = "Feb"
                    if month not in months:
                        print title, "==>", repr(datestring)
                        continue
                else:
                    print title, "==>", repr(datestring)
                    continue

            else:
                print "Unable to find date in ", title
                continue

            year = date.year
            month = months.index(month)+1
            if month < 9: year = year + 1
            date = datetime.date(year, month, int(day[:-2]))
             
            listings[title] = [date, ftitle, name, content[:20]]
                    
for t in listings:
#    print t, listings[t]
    pass
            

