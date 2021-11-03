from flask import Flask, render_template, redirect, request, flash
import sys
from networkx.algorithms import cluster
app = Flask(__name__)
app.secret_key = b'secretsecretsecret'
import pandas as pd
import numpy as np
import pickle
import networkx as nx
from math import radians, cos, sin, asin, sqrt
from sklearn.cluster import Birch


print("Loading food types...")
food_types = ['veg', 'non_veg', 'alcoholic_beverage', 'non_alcoholic_beverage', 'dessert']
food_types_clean = ['Vegetarian', 'Non-Vegetarian', 'Alcoholic beverages', 'Non-Alcoholic Beverages', 'Dessert']


df = pd.DataFrame()
cluster_data = pd.DataFrame()
avg_lat_long = pd.DataFrame()
results = pd.DataFrame()
adj_graph = nx.Graph()
model = Birch(n_clusters=100)
colours = []
col_map = dict()
type_map = dict()
locations = []
type_list = []



def initialisation_tasks():
    global df
    global cluster_data
    global avg_lat_long
    global adj_graph
    global model
    global colours
    global col_map
    global type_map
    global locations
    global type_list

    print("Loading csv files...")
    df = pd.read_csv("df_post_processing.csv")
    cluster_data = pd.read_csv("cluster_data.csv")
    avg_lat_long = df.groupby("location").mean()[["latitude", "longitude"]]

    print("Loading adjacency graph...")
    pickle_file = open('adj_graph_pickle.txt', "rb")
    adj_graph = pickle.load(pickle_file)

    print("Loading trained model...")
    model = pickle.load(open("birch_model.sav", 'rb'))

    print("Generating colour map for locations...")
    colours = []
    col_map = {}
    colour = 0
    location_list = []

    for location in df['location']:
        if location in col_map.keys():
            colours.append(col_map[location])
        else:
            col_map[location]=colour
            location_list.append(location)
            colours.append(colour)
            colour+=1

    locations = location_list
    
    type_no = 0
    type_map = {}
    type_arr = []
    type_list = []

    for listed_type in df['listed_in(type)']:
        if listed_type in type_map.keys():
            type_arr.append(type_map[listed_type])
        else:
            type_map[listed_type]=type_no
            type_list.append(listed_type)
            type_arr.append(type_no)
            type_no+=1
    




# Haversine formula for finding distances
def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8 # output in km

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c
    


@app.route("/") 
def home(): 
    global distance
    return render_template('home.html', distance=distance)

@app.route("/recommender")
def recommender():
    global locations
    global food_types
    global food_types_clean
    global type_list
    global results 

    zipped_file = zip(food_types, food_types_clean)
    return render_template('pref_input.html', locations=locations, zipped_file=zipped_file, type_list=type_list, results=results.iloc[:min(5, len(results))])


@app.route("/get_suggestions", methods=["POST"])
def get_suggestions():
    global col_map
    global type_map
    global model
    global cluster_data
    global results
    global df

    req = request.form
    flash("Made new request: "+str(req))

    # ['veg', 'non_veg', 'alcoholic_beverage', 'non_alcoholic_beverage', 'dessert']
    type_sel = req.getlist("type_sel")[0]
    dine_in = "dine_in" in req
    takeout = "takeout" in req
    rating = req.getlist("rating_input")[0]
    price_for_two = req.getlist("price")[0]

    if price_for_two == "":
        price_for_two = "500"


    location_sel = req.getlist("location_sel")[0]
    
    vegetarian = "veg" in req
    nonvegetarian = "non_veg" in req
    alcoholic_beverage = "alcoholic_beverage" in req
    non_alcoholic_beverage = "non_alcoholic_beverage" in req
    dessert = "dessert" in req

    app.logger.info("Got parameters:")

    idx = col_map[location_sel]

    preferences = [int(type_map[type_sel]), int(takeout), int(dine_in), float(rating), int(price_for_two), int(idx), float(avg_lat_long.iloc[idx]["latitude"]), float(avg_lat_long.iloc[idx]["longitude"]), int(vegetarian), int(nonvegetarian), int(alcoholic_beverage), int(non_alcoholic_beverage), int(dessert)]

    app.logger.info(preferences)

    indices = model_pred(model, cluster_data, preferences)["Unnamed: 0"]
    
    results = df.iloc[indices]
    results.drop(['Unnamed: 0'], axis=1, inplace=True)
    
    return redirect(request.referrer)   

@app.route("/setdistance", methods=["POST"])
def setdistance():
    global distance
    distance = float(request.form["distance"])
    flash("Made new request")
    print("set distance to", distance, file=sys.stderr)
    return redirect(request.referrer)   




def model_pred(model, df, preferences, ignore_dists=True):
    global cluster_data
    global avg_lat_long
    global adj_graph
    global colours
    global col_map

    location = preferences[5] #location as a number
    # app.logger.info(location)
    cluster = model.predict([preferences])
    bool_map = model.labels_==cluster
    results = df[np.array(bool_map,dtype=bool)]
    
    loc_name = list(col_map.keys())[list(col_map.values()).index(location)] 
    
    latitutde, longitude = preferences[6], preferences[7]
    loc_list = []
    for place in adj_graph.neighbors(loc_name):
        loc_list.append(place)
    loc_list.append(loc_name)

    loc_list_numbers = [col_map[x] for x in loc_list]

    # bool_map = results["location"] in loc_list_numbers
    results = results[results["location"].isin(loc_list_numbers)]
    # print(bool_map)
    # results = results[np.array(bool_map,dtype=bool)]

    if ignore_dists:
        return results

    distances = []
    for index, row in results.iterrows():
        dist = haversine(latitutde, longitude, row["latitude"], row["longitude"])
        distances.append(dist)

    results["dist"]=distances
    ouptut = results.sort_values(by=['dist'], ascending=False)
    return ouptut

if __name__ == '__main__':

    print("Running initialisation tasks...")
    initialisation_tasks()

    # print(model_pred(model, cluster_data, [0,1,1,5,800,0, 45.954851, -112.496595, 1,0,1,0,1]))


    print("Starting server on https://127.0.0.1:3000")
    app.run(host='127.0.0.1', port=3000, debug=True)