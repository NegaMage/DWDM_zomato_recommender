from flask import Flask, render_template, redirect, request, flash
import sys
app = Flask(__name__)
app.secret_key = b'secretsecretsecret'




distance = 0.1

locations = ['Domlur', 'Langford Town', 'Sankey Road', 'Basavanagudi', 'Jalahalli', 'Bommanahalli', 'Rammurthy Nagar', 'Electronic City', 'Vijay Nagar', 'Frazer Town', 'Ulsoor', 'Kaggadasapura', 'Koramangala 2nd Block', 'Nagawara', 'Brookefield', 'Basaveshwara Nagar', 'West Bangalore', 'Mysore Road', 'Sahakara Nagar', 'Yelahanka', 'HSR', 'Marathahalli', 'Uttarahalli', 'Wilson Garden', 'Ejipura', 'Sanjay Nagar', 'CV Raman Nagar', 'Yeshwantpur', 'Vasanth Nagar', 'HBR Layout', 'Infantry Road', 'South Bangalore', 'Richmond Road', 'RT Nagar', 'Old Airport Road', 'Koramangala 8th Block', 'Old Madras Road', 'New BEL Road', 'Rajajinagar', 'Magadi Road', 'Kanakapura Road', 'Koramangala 3rd Block', 'North Bangalore', 'Koramangala 5th Block', 'Kammanahalli', 'Church Street', 'Majestic', 'Jayanagar', 'Sadashiv Nagar', 'Sarjapur Road', 'Kumaraswamy Layout', 'Cunningham Road', 'Race Course Road', 'Jeevan Bhima Nagar', 'Brigade Road', 'Kalyan Nagar', 'Koramangala 7th Block', 'Bannerghatta Road', 'KR Puram', 'Koramangala', 'Banaswadi', 'Koramangala 6th Block', 'JP Nagar', 'Koramangala 4th Block', 'Banashankari', 'Shanti Nagar', 'East Bangalore', 'Thippasandra', 'Bellandur', 'Koramangala 1st Block', 'Lavelle Road', 'Varthur Main Road, Whitefield', 'Hosur Road', 'BTM', 'MG Road', 'Seshadripuram', 'Malleshwaram', 'Rajarajeshwari Nagar', 'Indiranagar', 'Residency Road', 'Central Bangalore', 'ITPL Main Road, Whitefield', 'St. Marks Road', 'Shivajinagar', 'City Market', 'Hennur', 'Commercial Street', 'Whitefield']

food_types = ["vegetarian", "non-vegetarian", "dairy", "desserts"]

@app.route("/") 
def home(): 
    global distance
    return render_template('home.html', distance=distance)

@app.route("/recommender")
def recommender():
    global locations
    return render_template('pref_input.html', locations=locations, food_types=food_types)

    app.logger.info("FUCK THIS", file=sys.stdout)

@app.route("/get_suggestions", methods=["POST"])
def get_suggestions():
    req = request.form
    flash("Made new request: "+str(req))

    location_sel = req.getlist("location_sel")[0]
    dine_in = "dine_in" in req
    takeout = "takeout" in req
    vegetarian = "vegetarian" in req
    nonvegetarian = "non-vegetarian" in req
    dairy = "dairy" in req
    desserts = "desserts" in req

    app.logger.info("Got parameters:\n")
    app.logger.info("Location: {}, dine_in: {}, takeout: {}, veg: {}, nonveg: {}, dairy: {}, desserts: {}".format(location_sel, dine_in, takeout, vegetarian, nonvegetarian, dairy, desserts))
    
    return redirect(request.referrer)   

@app.route("/testpage")
def testpage():
    global distance
    return render_template('page.html', distance=distance)

@app.route("/setdistance", methods=["POST"])
def setdistance():
    global distance
    distance = float(request.form["distance"])
    flash("Made new request")
    print("set distance to", distance, file=sys.stderr)
    return redirect(request.referrer)   



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)