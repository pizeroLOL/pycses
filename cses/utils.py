"""
该模块包含了一些用于内部处理的辅助函数。您也可以在您的代码中独立调用这些函数。
"""
import datetime


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
    return (day - start_day).days // 7 + 1
