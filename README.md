# DWDM Zomato Recommender

DWDM Project submitted by:

**Bhadra Giri** 181CO113

**Feyaz Baker** 181CO119

## Brief:
In this project, we looked at the [zomato dataset](https://www.kaggle.com/himanshupoddar/zomato-bangalore-restaurants), which contains a large amount of restaurants. From there, we cleaned and pared the data down, and augmented the data with location data, NLP for food item classification, and some feature extraction, to result in a dataframe. With the location data, we were able to generate an adjacency graph for all locations, and with all this information, we trained a model. This repo is just the frontend that takes the results of the [colab notebook here](https://colab.research.google.com/drive/1gQaFM9grXS3QIEm6Oahg08objzEmWS8R?usp=sharing&authuser=1#scrollTo=-bH38wnLr6YN), and presents the outputs with Flask and a few other libraries. All libraries used are in `requirements.txt`. 

## Warning: 

This project requires you to extract the accompanying `data.zip` and place the four files in the root of this folder. Those files were generated with the colab code [here](https://colab.research.google.com/drive/1gQaFM9grXS3QIEm6Oahg08objzEmWS8R?usp=sharing&authuser=1#scrollTo=-bH38wnLr6YN). 

Part of the colab code uses a Google Maps API, which is a paid product, and hence we haven't attached the key for the same. Because of this, some cells of the colab notebook are commented out entirely, but the rest of the notebook functions as expected.



## Instructions to execute:

1. Run `pip install -r requirements.txt` to install all the required libraries
2. Extract the contents of `data.zip` into this (root) folder
3. Start the server with `python3 server.py`.
4. Navigate to [127.0.0.1:3000](127.0.0.1:3000), and use the navbar. Enter your preferences, and scroll down to see the results.