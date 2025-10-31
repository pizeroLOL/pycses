"""
该模块包含了一些用于内部处理的辅助函数。您也可以在您的代码中独立调用这些函数。
"""
import datetime
import re
import logging
import reprlib
from sys import stderr

import yaml

logging.basicConfig(level=logging.DEBUG,
                    format="[{asctime} - {module}.{funcName}:{lineno}] \t{levelname}:\t {message}",
                    style="{",
                    stream=stderr)
log = logging.getLogger(__name__)
log.info(f"Loaded logger: {log!r}")

repr_ = reprlib.Repr(
    maxlevel=3, maxtuple=3, maxlist=3, maxarray=3, maxdict=3, maxset=3, maxfrozenset=3, maxdeque=3,
    maxstring=30, maxlong=50, maxother=30, fillvalue=' ... ', indent=None
).repr


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
            raise ValueError(f"Invalid time format for CSES format: {any_time!r}")
        else:
            res =  datetime.time(*map(int, matched.groups()))

    elif isinstance(any_time, int):  # 将秒数转换为时间对象
        res = datetime.time(any_time // 3600, (any_time // 60) % 60, any_time % 60)

    elif isinstance(any_time, datetime.time):  # 已经是datetime.time对象，直接返回
        res = any_time

    else:
        log.error(f"Unknown time type: {type(any_time)}, raising an error...")
        raise ValueError(f"Invalid time value for CSES format: {any_time}")

    return res


def serialize_time(dumper: yaml.representer.BaseRepresenter, any_time: datetime.time) -> yaml.nodes.ScalarNode:
    """
    适用于 ``datetime.time`` 对象的PyYAML钩子。

    Args:
        dumper: PyYAML Dumper对象，用于序列化
        any_time (datetime.time): 要转换的时间对象

    Returns:
        str: 对应的时间字符串，格式为 ``HH:MM:SS``
    """
    res = any_time.strftime("%H:%M:%S")
    return dumper.represent_scalar('tag:yaml.org,2002:str', res)
