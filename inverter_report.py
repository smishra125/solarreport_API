from flask import Flask
from flask_pymongo import PyMongo
import simplejson as json
from flask import request, jsonify
from flask_cors import CORS
import datetime as dt
import pytz
from datetime import datetime
from datetime import date
from inverter_utils import get_inverter_data
from daily_data import Daily
from weekly import Weekly
from monthly_data import MonthlyData
from yearly import Yearly


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/parserdb"
mongo = PyMongo(app)
CORS(app)


@app.route('/inverterdailyreport/', methods=['GET'])
def inverter_daily_data():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    if 'device_id' in request.args:
        deviceId = request.args['device_id']
    else:
        return jsonify({})

    if 'sdate' in request.args:
        startDateStr = request.args['sdate']
    else:
        return jsonify({})
    if 'edate' in request.args:
        endDateStr = request.args['edate']
    else:
        return jsonify({})

    start_time = " 06:30:00"
    end_time = " 23:00:00"

    starttimeStr = startDateStr + start_time
    start_date_start_obj = dt.datetime.strptime(starttimeStr, '%Y-%m-%d %H:%M:%S')
    endtimeStr = startDateStr + end_time
    start_date_end_obj = dt.datetime.strptime(endtimeStr, '%Y-%m-%d %H:%M:%S')

    end_date_start_timeStr = endDateStr + start_time
    end_date_start_obj = dt.datetime.strptime(end_date_start_timeStr, '%Y-%m-%d %H:%M:%S')

    end_date_end_timeStr = endDateStr + end_time
    end_date_end_obj = dt.datetime.strptime(end_date_end_timeStr, '%Y-%m-%d %H:%M:%S')

    timezone = pytz.timezone('Asia/Kolkata')

    start_date_start_timestamp = timezone.localize(start_date_start_obj)
    start_date_end_timestamp = timezone.localize(start_date_end_obj)
    end_date_start_timestamp = timezone.localize(end_date_start_obj)
    end_date_end_timestamp = timezone.localize(end_date_end_obj)

    daily_data_from_db, site_name = get_inverter_data(start_date_start_obj, start_date_end_obj, end_date_start_obj,
                                            end_date_end_obj, mongo, siteId, deviceId)

    data_report = Daily(daily_data_from_db)
    daily_data = data_report.get_daily_report()

    final_data = {
        "data": daily_data,
        "site_name": site_name
    }
    return jsonify(final_data)

@app.route('/inverterweeklyreport/', methods=['GET'])
def inverter_weekly_data():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    if 'sdate' in request.args:
        startDateStr = request.args['sdate']
    else:
        return jsonify({})
    if 'edate' in request.args:
        endDateStr = request.args['edate']
    else:
        return jsonify({})

    if 'device_id' in request.args:
        deviceId = request.args['device_id']
    else:
        return jsonify({})

    start_time = " 06:30:00"
    end_time = " 23:00:00"

    starttimeStr = startDateStr + start_time
    start_date_start_obj = dt.datetime.strptime(starttimeStr, '%Y-%m-%d %H:%M:%S')
    endtimeStr = startDateStr + end_time
    start_date_end_obj = dt.datetime.strptime(endtimeStr, '%Y-%m-%d %H:%M:%S')

    end_date_start_timeStr = endDateStr + start_time
    end_date_start_obj = dt.datetime.strptime(end_date_start_timeStr, '%Y-%m-%d %H:%M:%S')

    end_date_end_timeStr = endDateStr + end_time
    end_date_end_obj = dt.datetime.strptime(end_date_end_timeStr, '%Y-%m-%d %H:%M:%S')

    timezone = pytz.timezone('Asia/Kolkata')

    start_date_start_timestamp = timezone.localize(start_date_start_obj)
    start_date_end_timestamp = timezone.localize(start_date_end_obj)
    end_date_start_timestamp = timezone.localize(end_date_start_obj)
    end_date_end_timestamp = timezone.localize(end_date_end_obj)

    weekly_data_from_db, site_name = get_inverter_data(start_date_start_obj, start_date_end_obj, end_date_start_obj,
                                            end_date_end_obj, mongo, siteId, deviceId)


    data_report = Weekly(weekly_data_from_db)
    weekly_data = data_report.get_weekly_report()

    final_data = {
        "data": weekly_data,
        "site_name": site_name
    }
    return jsonify(final_data)

@app.route('/invertermonthlydata/', methods=['GET'])
def inverter_monthly_data():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    if 'device_id' in request.args:
        deviceId = request.args['device_id']
    else:
        return jsonify({})

    if 'sdate' in request.args:
        startDateStr = request.args['sdate']
    else:
        return jsonify({})
    if 'edate' in request.args:
        endDateStr = request.args['edate']
    else:
        return jsonify({})

    start_time = " 06:30:00"
    end_time = " 23:00:00"

    starttimeStr = startDateStr + start_time
    start_date_start_obj = dt.datetime.strptime(starttimeStr, '%Y-%m-%d %H:%M:%S')
    endtimeStr = startDateStr + end_time
    start_date_end_obj = dt.datetime.strptime(endtimeStr, '%Y-%m-%d %H:%M:%S')

    end_date_start_timeStr = endDateStr + start_time
    end_date_start_obj = dt.datetime.strptime(end_date_start_timeStr, '%Y-%m-%d %H:%M:%S')

    end_date_end_timeStr = endDateStr + end_time
    end_date_end_obj = dt.datetime.strptime(end_date_end_timeStr, '%Y-%m-%d %H:%M:%S')

    timezone = pytz.timezone('Asia/Kolkata')

    start_date_start_timestamp = timezone.localize(start_date_start_obj)
    start_date_end_timestamp = timezone.localize(start_date_end_obj)
    end_date_start_timestamp = timezone.localize(end_date_start_obj)
    end_date_end_timestamp = timezone.localize(end_date_end_obj)

    inverter_data_from_db, site_name = get_inverter_data(start_date_start_obj, start_date_end_obj, end_date_start_obj,
                                            end_date_end_obj, mongo, siteId, deviceId)

    data_report = MonthlyData(inverter_data_from_db)
    monthly_data = data_report.get_monthly_report()

    final_data = {
        "data": monthly_data,
        "site_name": site_name
    }
    return jsonify(final_data)

@app.route('/inverteryearlyreport/', methods=['GET'])
def inverter_yearly_data():
    if 'site_id' in request.args:
        siteId = int(request.args['site_id'])
    else:
        return jsonify({})

    if 'device_id' in request.args:
        deviceId = request.args['device_id']
    else:
        return jsonify({})

    if 'sdate' in request.args:
        startDateStr = request.args['sdate']
    else:
        return jsonify({})

    if 'edate' in request.args:
        endDateStr = request.args['edate']
    else:
        return jsonify({})

    start_time = " 6:30:00"
    end_time = " 23:00:00"

    starttimeStr = startDateStr + start_time
    start_date_start_obj = dt.datetime.strptime(starttimeStr, '%Y-%m-%d %H:%M:%S')
    endtimeStr = startDateStr + end_time
    start_date_end_obj = dt.datetime.strptime(endtimeStr, '%Y-%m-%d %H:%M:%S')

    end_date_start_timeStr = endDateStr + start_time
    end_date_start_obj = dt.datetime.strptime(end_date_start_timeStr, '%Y-%m-%d %H:%M:%S')

    end_date_end_timeStr = endDateStr + end_time
    end_date_end_obj = dt.datetime.strptime(end_date_end_timeStr, '%Y-%m-%d %H:%M:%S')

    timezone = pytz.timezone('Asia/Kolkata')

    start_date_start_timestamp = timezone.localize(start_date_start_obj)
    start_date_end_timestamp = timezone.localize(start_date_end_obj)
    end_date_start_timestamp = timezone.localize(end_date_start_obj)
    end_date_end_timestamp = timezone.localize(end_date_end_obj)

    monthly_data_from_db, site_name = get_inverter_data(start_date_start_obj, start_date_end_obj, end_date_start_obj,
                                                       end_date_end_obj, mongo, siteId, deviceId)

    data_report = Yearly(monthly_data_from_db)
    yearly_data = data_report.get_yearly_report()

    final_data = {
        "data": yearly_data,
        "site_name": site_name
    }
    return jsonify(final_data)


app.run(host="0.0.0.0")  # host to listen to all the ports
