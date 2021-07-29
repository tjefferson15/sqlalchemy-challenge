import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine('sqlite:///hawaii.sqlite')

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station 

session = Session(engine)

app= Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

 
    prcp_date_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date_list) 

@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)

    stations = {}

  
    results = session.query(Station.station, Station.name).all()
    for s,name in results:
        stations[s] = name

    session.close()
 
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine) 

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d') 

    results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year_date).\
                order_by(Measurement.date).all() 

    tobs_date_list = [] 
    for result in results:
        r = {}
        r["date"] = result[1]
        r["temprature"] = result[0]
        tobs_date_list.append(r)


    return jsonify(tobs_date_list)   



@app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
    
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

  
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).all()

    session.close()

    t_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_list.append(r)

  
    return jsonify(t_list)

@app.route("/api/v1.0/min_max_avg/<start>/<end>")
def start_end(start, end):
    
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end dates."""

  
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).filter(Measurement.date <= end_dt)

    session.close()

   
    t_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["EndDate"] = end_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_list.append(r)

    return jsonify(t_list)


if __name__ == "__main__":
    app.run(debug=True)














    