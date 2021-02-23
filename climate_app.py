from flask import Flask, jsonify

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

@app.route('/')
def home():
    return (
        f'Welcome to the Hawaii Climate Homepage!!'\
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>')

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
    session.close()
    return jsonify(st_results)

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

if __name__ == '__main__':
    app.run(debug = True)