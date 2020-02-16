#import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#create an engine to connect to the database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#create an app using flask...
vacation_app=Flask(__name__)

#create endpoint for the welcome page that lists all of the possible
@vacation_app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"/api/v1.0/start-date/start <br>"
        f"/api/v1.0/start-end/start*end"
        )

@vacation_app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query for the date and precipitation data for the last twelve months available
    twelve_months = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    #close the session
    session.close()
    #create an empty list to hold the dictionaries that will be created
    precipitations = []
    #use a for loop to create a dictionary with date as the key and precipitation as the value
    for date,prcp in twelve_months:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        #precipitation_dict["prcp"] = prcp
        precipitations.append(precipitation_dict)
    #the dictionaries are returned as json when a user navigates to the precipitation endpoint
    return jsonify(precipitations)

@vacation_app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query for the unique station ids
    station_id = session.query(Station.station).distinct().all()
    #close the session
    session.close()
    #create an empty list to hold the station ids
    stations = []
    #create a for loop to append each station id from the query to the list
    for station in station_id:
        stations.append(station.station)
    #this returs the list as jsonify when a user navigates to the stations endpoint
    return jsonify(stations)
  

@vacation_app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query for the date and observed temperature data for the last twelve months available
    year_of_temps = session.query(Measurement.date,Measurement.tobs).\
                        filter(Measurement.date>='2016-08-23').all()
    #close the session
    session.close()
    #create an empty list to hold the dictionaries that will be created
    temperatures = []
    #use a for loop to create a dictionary with date as the key and precipitation as the value
    for date,tobs in year_of_temps:
        temperature_dict = {}
        temperature_dict[date] = tobs
        #temperature_dict["tobs"] = tobs
        temperatures.append(temperature_dict)
    #the dictionaries are returned as json when a user navigates to the precipitation endpoint
    return jsonify(temperatures)

@vacation_app.route("/api/v1.0/start-date/<start>")
def vacation(start):
    #Create a session link from Python to the DB
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).\
                filter(Measurement.date == start).all()
    
    temp_values = []
    for temp in min_temp:
        min_temps_date = {}
        min_temps_date["minimum"] = temp
        temp_values.append(min_temps_date)
    
    max_temp = session.query(func.max(Measurement.tobs)).\
                filter(Measurement.date == start).all()

    for temp in max_temp:
        max_temps_date = {}
        max_temps_date["maximum"] = temp
        temp_values.append(max_temps_date)

    avg_temp = session.query(func.avg(Measurement.tobs)).\
                filter(Measurement.date == start).all()

    for temp in avg_temp:
        avg_temps_date = {}
        avg_temps_date["average"] = temp
        temp_values.append(avg_temps_date)

    session.close()

    return jsonify(temp_values)

           
@vacation_app.route("/api/v1.0/start-end/<start>*<end>")
def vacation_span(start,end):
    #Create a session link from Python to the DB
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    temp_values = []
    for temp in min_temp:
        min_temps_date = {}
        min_temps_date["minimum"] = temp
        temp_values.append(min_temps_date)
    
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    for temp in max_temp:
        max_temps_date = {}
        max_temps_date["maximum"] = temp
        temp_values.append(max_temps_date)

    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    for temp in avg_temp:
        avg_temps_date = {}
        avg_temps_date["average"] = temp
        temp_values.append(avg_temps_date)

    session.close()

    return jsonify(temp_values)
    
if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    vacation_app.run(debug=True)
