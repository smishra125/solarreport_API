from flask import Flask
from flask_pymongo import PyMongo
import simplejson as json
from flask import request, jsonify
from flask_cors import CORS
import datetime as dt
import pytz
from datetime import datetime
from weekly import Weekly
from monthly_utils import get_monthly_data


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/parserdb"
mongo = PyMongo(app)
CORS(app)

@app.route('/weeklyreport/', methods=['GET'])
def monthly_data():
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

    start_time = " 20:30:00"
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

    monthly_data_from_db, site_name = get_monthly_data(start_date_start_obj, start_date_end_obj, end_date_start_obj,
                                            end_date_end_obj, mongo, siteId)


    data_report = Weekly(monthly_data_from_db)
    weekly_data = data_report.get_weekly_report()

    final_data = {
        "data": weekly_data,
        "site_name": site_name
    }
    return jsonify(final_data)

app.run(host="0.0.0.0")  # host to listen to all the ports
