#!/usr/bin/env python

import MySQLdb as mdb
import sys
import re
import datetime
import os
from sets import Set

little = Set(["in","on","a","the","at","and"])
galleries = "/home/fisher/galleries"

def abort(msg):
    print >> sys.stderr, msg
    sys.exit(1)

class Screening(object):

    def __init__(self):
        self.title = None
        self.ftitle = None
        self.date = None
        self.name = None
        self.listing = None
        self.comments = None
        self.programme = None
        self.image = None

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

allImages = []
for dir in os.listdir(galleries):
    for f in os.listdir(os.path.join(galleries, dir)):
        allImages.append(os.path.join(galleries, dir, f))

comments= {}
programmes = {}
titpat = re.compile(r"(.*)\((.*)\)")
screenings = []

def getTitle(title):            
    ftitle = None
    m = titpat.match(title)                                                                                
    if m: title, ftitle = m.groups()
    return title, ftitle

posts = cur.fetchall()
for post in posts:
    title, name, date, content, category = post
    if len(content) < 10: continue
    if category in ["Newletters", "News items"]:
        pass
#        print title, name, category
    else:
        if category == "Listings":continue
        if "Listings" in category or "Screenings" in category:
            year = int(category[:4])
            category = "Listing"
        elif "Comments" in category:
            category = "Comments"
        elif "Programme" in category:
            category = "Programme"
        else:
            print "Odd category", category
            continue

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

            month = months.index(month)+1
            if month < 9: year = year + 1
            date = datetime.date(year, month, int(day[:-2]))
             
            screening = Screening()
            screening.title, screening.date, screening.ftitle, screening.name, screening.content = title, date, ftitle, name, content[:20]
            screenings.append(screening)
        
        elif category == "Programme":
            programmes[title] = content[:20]

        elif category == "Comments":
            comments[title] = content[:20]

for screening in screenings:
    if screening.title in programmes:
        screening.programme = programmes[screening.title]
        del programmes[screening.title]
    else:
        for title in programmes.keys():
            if title.lower().startswith(screening.title.lower()):
                screening.programme = programmes[title]
                del programmes[title]
                break
    if not screening.programme:
        print "No prog for ",  screening.title, screening.date
        
    if screening.title in comments:
        screening.comments = comments[screening.title]
        del comments[screening.title]
    else:
        for title in comments.keys():
            if title.lower().startswith(screening.title.lower()):
                screening.comments = comments[title]
                del comments[title]
                break
    if not screening.comments:
        print "No comments for ",  screening.title, screening.date

    dir = galleries + "/" + months[screening.date.month-1].lower()+str(screening.date.year)[2:]

    if not os.path.exists(dir): 
        continue

    twords = Set(screening.title.lower().split())
    if screening.ftitle: twords.update(Set(screening.ftitle.lower().split()))
    twords.difference_update(little)

    best = 0
    image = None
    for f in os.listdir(dir):
        s = f[:-4].lower()
        pwords = Set(s.split("_")) | Set(s.split("-")) - little - Set([s])
        num = len(pwords & twords)
        if num > best:
            image = dir + "/" + f
            best = num
    screening.image = image
    if not screening.image:
        print "Missing image", screening.title, screening.ftitle, screening.date
        for f in os.listdir(dir):
            s = f[:-4].lower()
            pwords = Set(s.split("_")) | Set(s.split("-")) - little - Set([s])

    else:
        if not image in allImages:
            print "Image already used", image
        else:
            allImages.remove(image)

print "\nSpare programes"
for t in programmes:
    print t

print "\nSpare comments"
for t in comments:
    print t

print "\nUnused images"
for image in allImages:
    print image
