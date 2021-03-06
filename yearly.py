import math
from datetime import datetime


class Yearly:
    response_json = {}

    def __init__(self, response_json):
        self.year_arr = []
        self.response_json = response_json
        for date_time_str in response_json['timestamp']:
            datetime_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            self.year_arr.append(datetime_object.year)

    def get_timestamp_range(self, start_year, end_year, year_list):
        """
        Take the first index of start_year and last index of end_year
        :param year_list: list of years fetched from mongodb query
        :param start_year: range start year
        :param end_year: range end year
        :return: index of start_year and index of end_year

        usage:
          >> get_timestamp_range(12, 2)
          >> (4, 8)
        """
        index_of_first_year = year_list.index(start_year)
        index_of_last_year = len(self.year_arr) - self.year_arr[::-1].index(end_year) - 1
        return index_of_first_year, index_of_last_year

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


    def get_sum_between_time_range(self, start_year, end_year, data_array):
        """
        :param start_year:
        :param end_year:
        :param data_array:
        :return:
            {
                "CUF": 12,
                "Energy": 100,
                ...
            }
        """
        start_range, end_range = self.get_timestamp_range(start_year, end_year, self.year_arr)
        return {
            "start_year": data_array["timestamp"][start_range],
            "end_year": data_array["timestamp"][end_range],
            "Energy"  : self.get_sum_from_list_block(start_range, end_range, data_array["energy"]),
            # "CUF"     : self.get_sum_from_list_block(start_range, end_range, data_array["CUF"], take_average=True),
            "PR"      : self.get_sum_from_list_block(start_range, end_range, data_array["PR"], take_average=True),
            # "Irradiance": self.get_sum_from_list_block(start_range, end_range, data_array["Irradiance"], take_average=True),
        }

    def get_yearly_report(self):
        yearly_data = []
        for year in list(set(self.year_arr)):
            start_year = year
            end_year = start_year
            try:
                yearly_data.append(self.get_sum_between_time_range(start_year, end_year, self.response_json))
            except (IndexError, ValueError):
                pass

        return yearly_data
