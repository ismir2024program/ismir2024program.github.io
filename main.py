# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
import glob
import json
import os
import pytz
from pytz import timezone
import tzlocal
import yaml
from flask import Flask, jsonify, redirect, render_template, send_from_directory
from flask_frozen import Freezer
from flaskext.markdown import Markdown
from dateutil import tz
import datetime

site_data = {}
by_uid = {}


def main(site_data_path):
    global site_data, extra_files
    extra_files = ["README.md"]
    # Load all for your sitedata one time.
    for f in glob.glob(site_data_path + "/*"):
        extra_files.append(f)
        name, typ = f.split("/")[-1].split(".")
        if typ == "json":
            site_data[name] = json.load(open(f))
        elif typ in {"csv", "tsv"}:
            site_data[name] = list(csv.DictReader(open(f)))
        elif typ == "yml":
            site_data[name] = yaml.load(open(f).read(), Loader=yaml.SafeLoader)

    for typ in ["papers", "speakers", "workshops", "tutorials", "lbd", "industry"]:
        by_uid[typ] = {}
        for p in site_data[typ]:
            by_uid[typ][p["UID"]] = p
    by_uid["days"] = {}
    site_data["days"] = []
    for day in ['1', '2', '3', '4', '5', '6']:
        speakers = [s for s in site_data["events"] if s["day"] == day and s["category"] == "All Meeting"]
        posters = [p for p in site_data["events"] if p["day"] == day and p["category"] == "Poster session"]
        lbd = [l for l in site_data["events"] if l["day"] == day and l["category"] == "LBD"]
        music = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Music"]
        industry = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Industry"]
        meetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Meetup"]
        vmeetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "VMeetup"]
        master = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Masterclass"]
        wimir = [w for w in site_data["events"] if w["day"] == day and w["category"] == "WiMIR Meetup"]
        special = [s for s in site_data["events"] if s["day"] == day and s["category"] == "Special Session"]
        opening = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Opening"]
        business = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Awards"]
        social = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Social"]
        tutorials = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Tutorials"]
        by_uid["days"][day] = {
            "uid": day,
            "speakers": speakers,
            "all": all,
            "meetup": meetup,
            "special": special,
            "master": master,
            "wimir": wimir,
            "posters": posters,
            "lbd": lbd,
            "music": music,
            "industry": industry,
            "day": day,
            "opening": opening,
            "business": business,
            "social": social,
            "vmeetup":vmeetup,
            "tutorials":tutorials
        }
        site_data["days"].append(by_uid["days"][day])

    print("Data Successfully Loaded")
    return extra_files


# ------------- SERVER CODE -------------------->

app = Flask(__name__)
app.config.from_object(__name__)
freezer = Freezer(app)
markdown = Markdown(app)


# MAIN PAGES


def _data():
    data = {}
    data["config"] = site_data["config"]
    return data


@app.route("/")
def index():
    return redirect("/index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(site_data_path, "favicon.ico")


# TOP LEVEL PAGES


# @app.route("/index.html")
# def home():
#     data = _data()
#     data["readme"] = open("README.md").read()
#     data["committee"] = site_data["committee"]["committee"]
#     return render_template("index.html", **data)
@app.route("/index.html")
def home():
    data = _data()
    data["day"] = {
        "speakers": site_data["speakers"],
        # "highlighted": [
        #     format_paper(by_uid["papers"][h["uid"]])
        # ],
    }
    return render_template("schedule.html", **data)

@app.route("/help.html")
def about():
    data = _data()
    data["FAQ"] = site_data["faq"]["FAQ"]
    return render_template("help.html", **data)


@app.route("/papers.html")
def papers():
    data = _data()
    data["papers"] = site_data["papers"]
    return render_template("papers.html", **data)

@app.route("/lbds.html")
def lbds():
    data = _data()
    data["lbds"] = site_data["lbd"]

    return render_template("lbds.html", **data)


@app.route("/paper_vis.html")
def paper_vis():
    data = _data()
    return render_template("papers_vis.html", **data)


@app.route("/calendar.html")
def schedule():
    data = _data()
    data["days"] = []
    # data = _data()
    for day in ['1', '2', '3', '4', '5', '6']:
        speakers = [s for s in site_data["events"] if s["day"] == day and s["category"] == "All Meeting"]
        posters = [p for p in site_data["events"] if p["day"] == day and p["category"] == "Poster session"]
        lbd = [l for l in site_data["events"] if l["day"] == day and l["category"] == "LBD"]
        music = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Music"]
        industry = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Industry"]
        meetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Meetup"]
        vmeetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "VMeetup"]
        master = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Masterclass"]
        wimir = [w for w in site_data["events"] if w["day"] == day and w["category"] == "WiMIR Meetup"]
        special = [s for s in site_data["events"] if s["day"] == day and s["category"] == "Special Session"]
        opening = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Opening"]
        business = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Awards"]
        social = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Social"]
        tutorials = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Tutorials"]
        out = {
            "speakers": speakers,
            "all": all,
            "meetup": meetup,
            "special": special,
            "master": master,
            "wimir": wimir,
            "posters": posters,
            "lbd": lbd,
            "music": music,
            "industry": industry,
            "day": day,
            "opening": opening,
            "business": business,
            "social": social,
            "vmeetup": vmeetup,
            "tutorials": tutorials

        }
        data["days"].append(out)
        
    return render_template("schedule.html", **data)


@app.route("/workshops.html")
def workshops():
    data = _data()
    data["workshops"] = [
        format_workshop(workshop) for workshop in site_data["workshops"]
    ]
    return render_template("workshops.html", **data)

@app.route("/tutorials.html")
def tutorials():
    data = _data()
    data["tutorials"] = site_data["tutorials"]
    return render_template("tutorials.html", **data)


@app.route("/industry.html")
def industry():
    data = _data()
    data["industry"] = site_data["industry"]
    return render_template("industry.html", **data)

@app.route("/industry_<uid>.html")
def industry_page(uid):
    data = _data()
    data["industry"] = by_uid["industry"][uid]
    return render_template("sponsor_booth.html", **data)

@app.route("/jobs.html") 
def jobs_page(): 
    data = _data() 
    data["industry"] = site_data["industry"]
    return render_template("jobs.html", **data)

@app.route("/tutorial_<tutorial>.html")
def tutorial(tutorial):
    uid = tutorial
    v = by_uid["tutorials"][uid]
    data = _data()
    data["tutorial"] = v
    return render_template("tutorial.html", **data)



def extract_list_field(v, key):
    value = v.get(key, "")
    if isinstance(value, list):
        return value
    else:
        return value.split("|")

def format_paper(v):

    list_keys = ["authors", "primary_subject", "secondary_subject", "session", "authors_and_affil"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)
    return {
        "id": v["UID"],
        "session": v["session"],
        "position": "{:02d}".format(int(v["position"])+1),
        "forum": v["UID"],
        "pic_id": v['thumbnail'],
        "content": {
            "title": v["title"],
            "paper_presentation": v["paper_presentation"],
            "long_presentation": v["long_presentation"],
            "authors": list_fields["authors"][0].split(";"),
            "authors_and_affil": list_fields["authors_and_affil"][0].split(";"),
            "keywords": list(set(list_fields["primary_subject"] + list_fields["secondary_subject"])),
            "abstract": v["Abstract"],
            "TLDR": v["Abstract"],
            "poster_pdf": v.get("poster_pdf", ""),
            "session": list_fields["session"],
            "pdf_path": v.get("pdf_path", ""),
            "video": v["video"],
            "channel_url": v["channel_url"],
            "slack_channel": v["slack_channel"],
            "slides_pdf": v.get("slides_pdf", ""),
            "day": v["day"],
            "review_1": v.get("Review 1", ""),
            "review_2": v.get("Review 2", ""),
            "review_3": v.get("Review 3", ""),
            "meta_review": v.get("Meta-review final summary", ""),
            "author_changes": v.get("Author description of changes", ""),
        },
        "poster_pdf": "GLTR_poster.pdf",
    }

def format_lbd(v):
    print(v)
    list_keys = ["authors", "primary_subject", "secondary_subject", "session", "authors_and_affil", "Author Names", "virtual?"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)
    return {
        "id": v["UID"],
        "forum": v["UID"],
        "pic_id": v['Thumbnail link'],
        "content": {
            "title": v["Paper Title"],
            "authors": list_fields["Author Names"][0].split(";"),
            "authors_and_affil": list_fields["authors_and_affil"][0].split(";"),
            "keywords": list(set(list_fields["primary_subject"] + list_fields["secondary_subject"])),
            "abstract": v["Abstract"],
            "TLDR": v["Abstract"],
            "poster_pdf": v.get("Poster link", ""),
            "session": list_fields["session"],
            "pdf_path": v.get("Paper link", ""),
            "video": v["Video link"],
            "channel_url": v["channel_url"],
            "slack_channel": v["slack_channel"],
            "virtual": v.get("virtual?", "0"),
            "virtual_slot1": v.get("virtual_slot1", "0"),
            "virtual_slot2": v.get("virtual_slot2", "0"),

        },
        "poster_pdf": "GLTR_poster.pdf",  
    }
  


def format_workshop(v):
    list_keys = ["authors"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "id": v["UID"],
        "title": v["title"],
        "organizers": list_fields["authors"],
        "abstract": v["abstract"],
    }


# ITEM PAGES

@app.route("/day_<day>.html")
def day(day):
    uid = day
    v = by_uid["days"][uid]
    data = _data()
    data["day"] = v
    data["daynum"] = uid
    return render_template("day.html", **data)

@app.route("/poster_<poster>.html")
def poster(poster):
    uid = poster
    v = by_uid["papers"][uid]
    data = _data()
    data["paper"] = format_paper(v)
    return render_template("poster.html", **data)


@app.route("/speaker_<speaker>.html")
def speaker(speaker):
    uid = speaker
    v = by_uid["speakers"][uid]
    data = _data()
    data["speaker"] = v
    return render_template("speaker.html", **data)


@app.route("/workshop_<workshop>.html")
def workshop(workshop):
    uid = workshop
    v = by_uid["workshops"][uid]
    data = _data()
    data["workshop"] = format_workshop(v)
    return render_template("workshop.html", **data)

@app.route("/lbd_<lbd>.html")
def lbd(lbd):
    uid = lbd
    v = by_uid["lbd"][uid]
    data = _data()
    data["lbd"] = format_lbd(v)
    return render_template("lbd.html", **data)


# FRONT END SERVING


@app.route("/papers.json")
def paper_json():
    json = []
    for v in site_data["papers"]:
        json.append(format_paper(v))
    return jsonify(json)




@app.route("/lbds.json")
def lbd_json():
    json = []
    for v in site_data["lbd"]:
        json.append(format_lbd(v))
    return jsonify(json)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/serve_<path>.json")
def serve(path):
    return jsonify(site_data[path])



@app.template_filter('localcheck')
def datetimelocalcheck(s):
    return tzlocal.get_localzone()

@app.template_filter('localizetime')
def localizetime(date,time,timezone):
    to_zone = tz.gettz(str(timezone))
    date = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
    ref_date_tz = pytz.timezone('America/Los_Angeles').localize(date) #[TODO] take ref time zone as input
    local_date = ref_date_tz.astimezone(to_zone)
    return local_date.strftime("%Y-%m-%d"), local_date.strftime("%H:%M")



# --------------- DRIVER CODE -------------------------->
# Code to turn it all static


@freezer.register_generator
def generator():
    for paper in site_data["papers"]:
        yield "poster", {"poster": str(paper["UID"])}
    for speaker in site_data["speakers"]:
        yield "speaker", {"speaker": str(speaker["UID"])}
    for workshop in site_data["workshops"]:
        yield "workshop", {"workshop": str(workshop["UID"])}
    for tutorial in site_data["tutorials"]:
        yield "tutorial", {"tutorial": str(tutorial["UID"])}
    for day in site_data["days"]:
        yield "day", {"day": str(day["uid"])}
    for lbd in site_data["lbd"]:
        yield "lbd", {"lbd": str(lbd["UID"])}
    for industry in site_data["industry"]:
        yield "industry_page", {"uid": str(industry["UID"])}

    for key in site_data:
        if key != 'days':
            yield "serve", {"path": key}


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")

    parser.add_argument(
        "--build",
        action="store_true",
        default=False,
        help="Convert the site to static assets",
    )

    parser.add_argument(
        "-b",
        action="store_true",
        default=False,
        dest="build",
        help="Convert the site to static assets",
    )

    parser.add_argument("path", help="Pass the JSON data path and run the server")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    site_data_path = args.path
    extra_files = main(site_data_path)

    if args.build:
        freezer.freeze()
    else:
        debug_val = False
        if os.getenv("FLASK_DEBUG") == "True":
            debug_val = True

        app.run(port=5000, debug=debug_val, extra_files=extra_files)
