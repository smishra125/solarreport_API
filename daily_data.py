import math
from datetime import datetime


class Daily:
    response_json = {}

    def __init__(self, response_json):
        self.day_arr = []
        self.response_json = response_json
        for date_time_str in response_json['timestamp']:
            datetime_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            self.day_arr.append(datetime_object.day)

    def get_timestamp_range(self, start_day, end_day, day_list):
        """
        Take the first index of start_day and last index of end_day
        :param day_list: list of days fetched from mongodb query
        :param start_day: range start day
        :param end_day: range end day
        :return: index of start_day and index of end_day

        usage:
          >> get_timestamp_range(12, 2)
          >> (4, 8)
        """
        index_of_first_day = day_list.index(start_day)
        index_of_last_day = len(self.day_arr) - self.day_arr[::-1].index(end_day) - 1
        return index_of_first_day, index_of_last_day

    @staticmethod
    def get_sum_from_list_block(start_range, end_range, resultant_array, take_average=False):
        sliced_array = resultant_array[start_range:end_range + 1]

        final_sum = 0
        for each_value in sliced_array:
            try:
                final_sum += float(each_value) if not math.isnan(float(each_value)) else 0
            except (TypeError, SyntaxError):
                continue
        try:
            return final_sum if not take_average else final_sum/sliced_array.__len__()
        except ZeroDivisionError:
            return 0


    def get_sum_between_time_range(self, start_day, end_day, data_array):
        """
        :param start_day:
        :param end_day:
        :param data_array:
        :return:
            {
                "CUF": 12,
                "Energy": 100,
                ...
            }
        """
        start_range, end_range = self.get_timestamp_range(start_day, end_day, self.day_arr)
        return {
            "start_day": data_array["timestamp"][start_range],
            "end_day": data_array["timestamp"][end_range],
            "Energy"  : self.get_sum_from_list_block(start_range, end_range, data_array["energy"]),
            # "CUF"     : self.get_sum_from_list_block(start_range, end_range, data_array["CUF"], take_average=True),
            "PR"      : self.get_sum_from_list_block(start_range, end_range, data_array["PR"], take_average=True),
            # "Irradiance": self.get_sum_from_list_block(start_range, end_range, data_array["Irradiance"], take_average=True),
        }

    def get_daily_report(self):
        daily_data = []
        for day in list(set(self.day_arr)):
            start_day = day
            end_day = start_day
            try:
                daily_data.append(self.get_sum_between_time_range(start_day, end_day, self.response_json))
            except (IndexError, ValueError):
                pass

        return daily_data
