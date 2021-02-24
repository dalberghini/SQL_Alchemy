from flask import Flask, json, jsonify

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f'Welcome to the Hawaii Climate Homepage!!<br/>'
        f'Available Routes: <br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'For the above method, choose a starting date to get the Minimum Temperature, Maximum Temperature and the Average Temperature in the following format YYYY,MM,DD.<br/>'
        f'/api/v1.0/<start>/<end><br/>'
        f'For the above path, choose a starting date in the YYYY,MM,DD format and then a / and then choose an ending date in the YYYY,MM,DD format to get the Minimum Temperature, Maximum Temperature and Average Temperature between those days. Happy Searching.'
        )

@app.route('/api/v1.0/precipitation')
def precipation():
    session = Session(engine)
    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016,8,23)).all()
    session.close()
    rainfall = dict((results))

    return jsonify(rainfall)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    st_results = session.query(Measurement.station).group_by(Measurement.station).all()
    station_results = list(np.ravel(st_results))
    session.close()
    return jsonify(station_results)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    sel = [Measurement.station, func.count(Measurement.station)]
    stat= session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active_station = stat[0][0]
    most_active_data = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station == most_active_station).filter(Measurement.date >= dt.date(2016,8,23)).all()
    active_resluts = dict(most_active_data)
    session.close()
    return jsonify(active_resluts)

@app.route('/api/v1.0/<start>')
def start(start):
    canonicalized = start.replace(",","-")
    session = Session(engine)
    something = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    start_query = session.query(*something).filter(Measurement.date >= (canonicalized)).all()
    session.close()
    start_list = []
    for tmin, tmax, tavg in start_query:
        tagg_dict = {}
        tagg_dict["TMIN"] = tmin
        tagg_dict["TMAX"] = tmax
        tagg_dict["TAVG"] = tavg
        start_list.append(tagg_dict)
    return(jsonify(start_list))

@app.route('/api/v1.0/<start>/<end>')
def end_date(start, end):
    canonicalized = start.replace(",","-")
    canonicalized1 = end.replace(",","-")
    session = Session(engine)
    something = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    end_query = session.query(*something).filter(Measurement.date.between(canonicalized, canonicalized1)).all()
    session.close()
    end_list = []
    for tmin, tmax, tavg in end_query:
        tagg_dict = {}
        tagg_dict["TMIN"] = tmin
        tagg_dict["TMAX"] = tmax
        tagg_dict["TAVG"] = tavg
        end_list.append(tagg_dict)
    return(jsonify(end_list))


if __name__ == '__main__':
    app.run(debug = True)