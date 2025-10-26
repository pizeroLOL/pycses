"""
该模块包含了一些用于内部处理的辅助函数。您也可以在您的代码中独立调用这些函数。
"""
import datetime
import re
import logging


logging.basicConfig(level=logging.DEBUG,
                    format="[{asctime} - {module}:{lineno}] {levelname}: {message}",
                    style="{")
log = logging.getLogger(__name__)


def week_num(start_day: datetime.date, day: datetime.date) -> int:
    """
    计算指定日期是从开始日期开始的第多少周。

    Args:
        day (datetime.date): 要计算周次的日期
        start_day (datetime.date): 课程开始的日期，用于计算周次

    Returns:
        int: 指定日期是从开始日期开始的第多少周

    Examples:
        >>> week_num(datetime.date(2025, 9, 1), datetime.date(2025, 9, 4))
        1
        >>> week_num(datetime.date(2025, 9, 1), datetime.date(2025, 9, 16))
        3
        >>> week_num(datetime.date(2025, 9, 1), datetime.date(2025, 10, 24))
        8
    """
    res = (day - start_day).days // 7 + 1
    log.debug(f"Calling week_num({start_day}, {day}) -> {res}")
    return res


def ensure_time(any_time: str | int | datetime.time) -> datetime.time:
    """
    将时间字符串/整数值转换为 ``datetime.time`` 对象。

    Args:
        any_time (str | int | datetime.time): 时间字符串，格式为 ``HH:MM:SS`` 或一个表示一天中经过的秒数的整数。

    Returns:
        datetime.time: 对应的时间对象

    Examples:
        >>> ensure_time("08:00:00")
        datetime.time(8, 0)
        >>> ensure_time(10*3600 + 10*60 +10)  # =36610
        datetime.time(10, 10, 10)
    """

    pattern_for_str = re.compile(r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)")  # CSES Schema 指定的时间格式

    if isinstance(any_time, str):  # 使用regex处理字符串格式的时间
        if not (matched := pattern_for_str.match(any_time)):
            raise ValueError(f"Invalid time format for CSES format: {any_time}")
        else:
            return datetime.time(*map(int, matched.groups()))

    elif isinstance(any_time, int):  # 将秒数转换为时间对象
        return datetime.time(any_time // 3600, (any_time // 60) % 60, any_time % 60)

    elif isinstance(any_time, datetime.time):  # 已经是datetime.time对象，直接返回
        return any_time

    else:
        raise ValueError(f"Invalid time value for CSES format: {any_time}")
