import datetime
from datetime import datetime

import pandas as pd

from Utils.FileUtils import FileUtils


def is_date_actual(date_to_check, last_date_file="", last_date="", date_time_format="%d.%m.%Y um %H:%M"):
    """

    :param date_time_format:
    :type last_date: object
    :param last_date_file:
    :param date_to_check:
    :return:
    """

    if date_to_check is None:
        raise NotImplementedError

    if last_date == "":
        if FileUtils.check_file_exists_or_create(last_date_file, "last_check_date"):  # no need to check, creates anyway
            data = pd.read_csv(last_date_file)
            last_date_str = str(data.last_check_date[0])
            last_date = datetime.strptime(last_date_str, date_time_format)
        else:
            return False, ""

    is_news_current= last_date < date_to_check

    if is_news_current:
        with open(last_date_file, "w") as myfile:
            myfile.write("last_check_date" + "\n")
            datetime_object_str = datetime.strftime(date_to_check, date_time_format)
            myfile.write(str(datetime_object_str) + "\n")
            return is_news_current, date_to_check

    return is_news_current, last_date


