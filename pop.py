#!/usr/bin/env python

import MySQLdb as mdb
import sys
import re
import datetime
import time
import os
from sets import Set
import shutil
import subprocess

galleries = "/home/fisher/galleries"
username = 'root'
schemain = 't'
schemaout = 'wp'
dbhost = 'localhost'
base = '/var/www/html'

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
        self.scores = None

args = sys.argv[1:]
if len(args) != 1: abort("Must have one argument")
password = args[0]

shutil.rmtree(os.path.join(base, "wp-content", "uploads"), True)

little = Set(["in","on","a","the","at","and"])
months =  ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

conin = mdb.connect(dbhost, username, password, schemain)
curin = conin.cursor()
conout = mdb.connect(dbhost, username, password, schemaout)
curout = conout.cursor()

curout.execute("delete from wp_posts where post_type != 'acf'")
curout.execute("select id from wp_posts")
acfid = curout.fetchall()[0][0]
curout.execute("delete from wp_postmeta where post_id != " + str(acfid))
curout.execute("delete from wp_term_relationships")

count = curin.execute("select p.post_title, p.post_name, p.post_date, p.post_content, t.name from wp_posts p, wp_term_relationships r, wp_term_taxonomy x, wp_terms t where x.term_id = t.term_id and r.term_taxonomy_id = x.term_taxonomy_id and r.object_id = p.id and post_status = 'publish' and post_type='post' order by p.post_title")

allImages = []
for dir in os.listdir(galleries):
    for f in os.listdir(os.path.join(galleries, dir)):
        allImages.append(os.path.join(galleries, dir, f))

comments= {}
programmes = {}
titpat = re.compile(r"(.*)\((.*)\)")
wh = re.compile(r"^.* JPEG (\d+)x(\d+) .*")
screenings = []

def getTitle(title):
    ftitle = None
    m = titpat.match(title)
    if m: title, ftitle = m.groups()
    return title, ftitle

posts = curin.fetchall()
curout.execute("select max(id) from wp_posts");
postid = curout.fetchall()[0][0]+1
curout.execute("select term_id from wp_terms where name = 'Newsletters'")
termid = curout.fetchall()[0][0]
newscount = 0
for post in posts:
    title, name, date, content, category = post
    if len(content) < 10: continue
    if category in ["News items"]:
        pass
    elif category in ["Newletters"]:
        tuple = (postid, date, date, content, title, name, date, date, "/?p=" + str(postid))
        curout.execute("""insert into wp_posts (id, post_author, post_date, post_date_gmt, post_content, post_title,
        post_excerpt, post_status, comment_status, ping_status, post_name,  to_ping, pinged, post_modified, post_modified_gmt,
        post_content_filtered, guid, post_type, post_mime_type)
        values (%s, 1, %s, %s, %s, %s, '', 'publish',
        'closed', 'closed', %s, '', '', %s, %s, '', %s, 'post', '' )""", tuple)
        tuple = (postid, termid)
        curout.execute("""insert into wp_term_relationships (object_id, term_taxonomy_id) values(%s, %s)""", tuple)
        postid += 1
        newscount += 1
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
            screening.title, screening.date, screening.ftitle, screening.name, screening.content = title, date, ftitle, name, content
            screenings.append(screening)

        elif category == "Programme":
            programmes[title] = content

        elif category == "Comments":
            comments[title] = content

curout.execute("update wp_term_taxonomy set count = " + str(newscount) + " where term_taxonomy_id = " + str(termid))
# Read the scores into allscores list
allscores = []
f = open("scores.txt")
for l in f.readlines():
    bits = l.split(",")
    if len(bits) != 7: abort("Too many commas " + l)
    name = bits[0].lower()
    scores = bits[1:6]
    bits = name.split()
    daterange = bits[0]
    sorf = bits[1]
    name = Set(bits[2:]) - little
    allscores.append((name, daterange, sorf, scores, " ".join(bits[2:])))
f.close()

# Look for a match between a score and a film
for n in range(4, 0, -1):
    for screening in screenings:
        twords = Set(screening.title.lower().split()) - little
        bestmatch = 0
        for score in allscores:
            match = len(twords & score[0])
            if match > bestmatch:
                bestmatch = match
                bestscore = score
        if bestmatch == len(twords) or (bestmatch >= n and n > 1):
            screening.scores = bestscore[3]
            allscores.remove(bestscore)

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

    if not screening.scores:
        print "Missing scores", screening.title, screening.ftitle, screening.date

print "\nSpare programes"
for t in programmes:
    print t

print "\nSpare comments"
for t in comments:
    print t

print "\nUnused images"
for image in allImages:
    print image

print "\nUnused scores"
for s in allscores:
    print s[4], s[1], s[2]

print "Now start importing", len(screenings), "screenings"
curout.execute("select max(meta_id) from wp_postmeta");
postmetaid = curout.fetchall()[0][0]+1

for screening in screenings:
    year = screening.date.year
    month = screening.date.month
    drel =  os.path.join("wp-content", "uploads", str(year), str(month))
    if screening.image:
        image =  '<img class=" wp-image-428 alignleft" src="' + os.path.join("/", drel, os.path.basename(screening.image)) +'" alt="' + screening.name + '" width="400" height="266" />'
    else:
        image = ''

    tuple = (postid, image + screening.content, screening.title, screening.name, "/?post_type=screening&#038;p=" + str(postid))

    curout.execute("""insert into wp_posts (id, post_author, post_date, post_date_gmt, post_content, post_title,
        post_excerpt, post_status, comment_status, ping_status, post_name,  to_ping, pinged, post_modified, post_modified_gmt,
        post_content_filtered, guid, post_type, post_mime_type) values (%s, 1, now(), now(), %s, %s, '', 'publish',
        'closed', 'closed', %s, '', '', now(), now(), '', %s, 'screening', '' )""", tuple)

    tuples = [(postmetaid, postid, 'datetime',  str(int(time.mktime(screening.date.timetuple())))),
              (postmetaid + 1, postid, '_datetime', 'field_5831ced85298d')]
    postmetaid += 2
    if screening.programme:
        tuples.extend([(postmetaid, postid, 'notes', screening.programme),
                  (postmetaid + 1, postid, '_notes', 'field_5831d68620cc4')])
        postmetaid += 2
    if screening.comments:
        tuples.extend([(postmetaid, postid, 'comments', screening.comments),
              (postmetaid + 1, postid, '_comments', 'field_5831d6c520cc5')])
        postmetaid += 2
    if screening.ftitle:
        tuples.extend([(postmetaid, postid, 'aka', screening.ftitle),
              (postmetaid + 1, postid, '_aka', 'field_58472e6b4230d')])
        postmetaid += 2
    if screening.scores:
        tuples.extend([(postmetaid, postid, 'as', screening.scores[0]),
              (postmetaid + 1, postid, '_as', 'field_5831d6f120cc6'),
              (postmetaid + 2, postid, 'bs', screening.scores[1]),
              (postmetaid + 3, postid, '_bs', 'field_5831d72220cc7'),
              (postmetaid + 4, postid, 'cs', screening.scores[2]),
              (postmetaid + 5, postid, '_cs', 'field_5838d1a9da65e'),
              (postmetaid + 6, postid, 'ds', screening.scores[3]),
              (postmetaid + 7, postid, '_ds', 'field_5838d1f4da660'),
              (postmetaid + 8, postid, 'es', screening.scores[4]),
              (postmetaid + 9, postid, '_es', 'field_5838d20cda661')])
        postmetaid += 10
    curout.executemany("insert into wp_postmeta (meta_id, post_id, meta_key, meta_value) values (%s, %s, %s, %s)", tuples)

    mainPostId = postid
    postid += 1

    if screening.image:
        d = os.path.join(base, drel)
        loc =  os.path.join(str(year), str(month), os.path.basename(screening.image))
        try: os.makedirs(d)
        except: pass
        shutil.copy(screening.image, d)
        line = subprocess.check_output (["identify", screening.image])
        m = wh.match(line)
        if m:
            w, h = m.groups()
        else:
            abort("Can't parse " + line)
        tuple = (postid, screening.name, screening.name, os.path.join(drel, os.path.basename(screening.image)))

        curout.execute("""insert into wp_posts (id, post_author, post_date, post_date_gmt, post_content, post_title,
        post_excerpt, post_status, ping_status, post_name,  to_ping, pinged, post_modified, post_modified_gmt,
        post_content_filtered, guid, post_type, post_mime_type) values (%s, 1, now(), now(), '', %s, '', 'inherit',
        'closed', %s, '', '', now(), now(), '', %s, 'attachment', 'image/jpeg' )""", tuple)

        md = 'a:4:{s:5:"width";i:' + w + ';s:6:"height";i:' + h + ';s:4:"file";s:' + str(len(loc)) + ':"' + loc + '";s:10:"image_meta";a:12:{s:8:"aperture";s:1:"0";s:6:"credit";s:0:"";s:6:"camera";s:0:"";s:7:"caption";s:0:"";s:17:"created_timestamp";s:1:"0";s:9:"copyright";s:0:"";s:12:"focal_length";s:1:"0";s:3:"iso";s:1:"0";s:13:"shutter_speed";s:1:"0";s:5:"title";s:0:"";s:11:"orientation";s:1:"0";s:8:"keywords";a:0:{}}}'
        tuples = [(postmetaid, postid,  '_wp_attached_file', loc),
                  (postmetaid + 1, postid, '_wp_attachment_metadata', md)]
        curout.executemany("insert into wp_postmeta (meta_id, post_id, meta_key, meta_value) values (%s, %s, %s, %s)", tuples)
        postmetaid += 2
        postid += 1

conin.close()
conout.commit()
conout.close()
