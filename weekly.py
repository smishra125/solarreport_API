import math
from datetime import datetime


class Weekly:
    response_json = {}

    def __init__(self, response_json):
        self.week_arr = []
        self.response_json = response_json
        for date_time_str in response_json['timestamp']:
            datetime_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            self.week_arr.append(datetime_object.strftime("%U"))

    def get_timestamp_range(self, start_week, end_week, week_list):
        """
        Take the first index of start_week and last index of end_week
        :param week_list: list of weeks fetched from mongodb query
        :param start_week: range start week
        :param end_week: range end week
        :return: index of start_week and index of end_week

        usage:
          >> get_timestamp_range(12, 2)
          >> (4, 8)
        """
        index_of_first_week = week_list.index(start_week)
        index_of_last_week = len(self.week_arr) - self.week_arr[::-1].index(end_week) - 1
        return index_of_first_week, index_of_last_week

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


    def get_sum_between_time_range(self, start_week, end_week, data_array):
        """
        :param start_week:
        :param end_week:
        :param data_array:
        :return:
            {
                "CUF": 12,
                "Energy": 100,
                ...
            }
        """
        start_range, end_range = self.get_timestamp_range(start_week, end_week, self.week_arr)
        return {
            "start_week": data_array["timestamp"][start_range],
            "end_week": data_array["timestamp"][end_range],
            "Energy"  : self.get_sum_from_list_block(start_range, end_range, data_array["energy"]),
            # "CUF"     : self.get_sum_from_list_block(start_range, end_range, data_array["CUF"], take_average=True),
            "PR"      : self.get_sum_from_list_block(start_range, end_range, data_array["PR"], take_average=True),
            # "Irradiance": self.get_sum_from_list_block(start_range, end_range, data_array["Irradiance"], take_average=True),
        }

    def get_weekly_report(self):
        weekly_data = []
        for week in list(set(self.week_arr)):
            start_week = week
            end_week = start_week
            try:
                weekly_data.append(self.get_sum_between_time_range(start_week, end_week, self.response_json))
            except (IndexError, ValueError):
                pass

        return weekly_data
