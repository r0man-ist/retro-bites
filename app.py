from flask import Flask, request, render_template, redirect, url_for, abort, jsonify
import json


app = Flask(__name__)
app.config['FREEZER_BASE_URL'] = 'https://r0man-ist.github.io/retro-bites/'
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'

@app.route("/", methods=["GET"])
def index():
    with open("static/db.json", "r", encoding="utf-8") as f:
        COLLECTION = json.load(f)
    
    return render_template("index.html", menucards=COLLECTION)

# no longer needed (?)
"""@app.route("/item/default")
def empty_item_redirect():
    with open("static/db.json", "r", encoding="utf-8") as f:
        COLLECTION = json.load(f)
    # Redirect to the item with ID 1
    return redirect(url_for('item_nr', item_id=4))"""

@app.route("/item/<int:item_id>/")
def item_nr(item_id):
    with open("static/db.json", "r", encoding="utf-8") as f:
        COLLECTION = json.load(f)

    # Find the item with the given ID
    item = next((item for item in COLLECTION if item["id"] == item_id), None)
    
    if item is None:
        abort(404)  # Item not found, return a 404 error

        
    return render_template("item.html", item=item,  _external=True)

# api endpoint to get item details by ID
@app.route('/api/item/<int:item_id>/')
def item_api(item_id):
    with open("static/db.json", "r", encoding="utf-8") as f:
        COLLECTION = json.load(f)

    # Find the item with the given ID
    item = next((item for item in COLLECTION if item["id"] == item_id), None)
    
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item)
    

@app.route('/api/locations/')
def locations():
    with open("static/db.json", "r", encoding="utf-8") as f:
       COLLECTION = json.load(f)
    # Extract unique locations from the collection
    unique_locations = {}
    for item in COLLECTION:
        place = item.get('place')
        if place:
            lat = place.get('lat')
            long = place.get('long')
            name = place.get('Name')
            if lat and long and name:
                unique_locations[name] = {'lat': lat, 'long': long}
    # Return the unique locations as JSON
    return jsonify(unique_locations)
   

@app.route("/sammlung/")
def sammlung():
    return render_template("collection.html")

@app.route("/data/")
def data():
    return render_template("data.html")

@app.route("/team/")
def team():
    return render_template("team.html")