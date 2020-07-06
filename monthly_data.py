import math
from datetime import datetime


class MonthlyData:
    response_json = {}

    def __init__(self, response_json):
        self.month_arr = []
        self.response_json = response_json
        for date_time_str in response_json['timestamp']:
            datetime_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            self.month_arr.append(datetime_object.month)

    def get_timestamp_range(self, start_month, end_month, month_list):
        """
        Take the first index of start_month and last index of end_month
        :param month_list: list of months fetched from mongodb query
        :param start_month: range start month
        :param end_month: range end month
        :return: index of start_month and index of end_month

        usage:
          >> get_timestamp_range(12, 2)
          >> (4, 8)
        """
        index_of_first_month = month_list.index(start_month)
        index_of_last_month = len(self.month_arr) - self.month_arr[::-1].index(end_month) - 1
        return index_of_first_month, index_of_last_month

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

    def get_sum_between_time_range(self, start_month, end_month, data_array):
        """
        :param start_month:
        :param end_month:
        :param data_array:
        :return:
            {
                "CUF": 12,
                "Energy": 100,
                ...
            }
        """
        start_range, end_range = self.get_timestamp_range(start_month, end_month, self.month_arr)
        return {
            "start_month": data_array["timestamp"][start_range],
            "end_month": data_array["timestamp"][end_range],
            "Energy"     : self.get_sum_from_list_block(start_range, end_range, data_array["energy"]),
            "CUF": self.get_sum_from_list_block(start_range, end_range, data_array["CUF"], take_average=True),
            "PR": self.get_sum_from_list_block(start_range, end_range, data_array["PR"], take_average=True),
            # "Irradiance": self.get_sum_from_list_block(start_range, end_range, data_array["Irradiance"], take_average=True)
        }

    def get_monthly_report(self):
        monthly_data = []
        for month in list(set(self.month_arr)):
            start_month = month
            end_month = start_month
            try:
                monthly_data.append(self.get_sum_between_time_range(start_month, end_month, self.response_json))
            except (IndexError, ValueError):
                pass
        return monthly_data
