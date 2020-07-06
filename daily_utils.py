from datetime import timedelta


def get_daily_data(start_date_start_obj, start_date_end_obj, end_date_start_obj, end_date_end_obj,
                     mongo_connection, site_id):


    current_start_timestamp = start_date_start_obj
    current_end_timestamp = start_date_end_obj

    final_result = {
        "timestamp": [],
        "energy" : [],
        "irradiation": [],
        "CUF": [],
        "PR": []
    }

    site = list(mongo_connection.db.m_site.find({"$and": [{"site_id": site_id}, ]}))

    while current_start_timestamp <= end_date_start_obj and current_end_timestamp <= end_date_end_obj:
        current_start_epoch_time = current_start_timestamp.strftime('%s')
        current_end_epoch_time = current_end_timestamp.strftime('%s')

        plant_record = list(mongo_connection.db.plant_history.find({"$and": [{"site_id": site_id},
                                                                            {"record_timestamp": {
                                                                                "$gte": int(current_start_epoch_time)}},
                                                                            {
                                                                                "record_timestamp":
                                                                                    {
                                                                                        "$lte": int(current_end_epoch_time)
                                                                                    }
                                                                            }, {"p_today_energy":{"$gt":0}}
                                                                            ]
                                                                   }, {
            '_id': 0, "p_today_energy": 1, "record_time": 2, "p_pr": 3}).sort("record_time", -1).limit(1))

        # wst = list(
        #     mongo_connection.db.wst_history.find({"$and": [{"site_id": site_id}, {"record_timestamp": {"$gte": int(current_start_epoch_time)}},
        #                                                    {"record_timestamp": {"$lte": int(current_end_epoch_time)}}]},
        #                                          {'_id': 0, "irradiation": 1}).limit(1))

        current_start_timestamp += timedelta(days=1)
        current_end_timestamp += timedelta(days=1)

        for each_data in plant_record:
            final_result["timestamp"].append(each_data.get("record_time", 0))
            final_result["energy"].append(each_data.get("p_today_energy", 0))
            final_result["PR"].append(each_data.get("p_pr", 0))
            final_result["CUF"].append(0)

        # for each_data in wst:
        #     final_result["irradiation"].append(each_data.get('irradiation', 0))

    return final_result, site[0]["site_name"]