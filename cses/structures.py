import datetime
from enum import Enum

from pydantic import BaseModel

import cses.utils as utils


class Subject(BaseModel):
    """
    单节课程科目。

    Args:
        name (str): 科目名称，如“语文”
        simplified_name (str): 科目简化名称，如“语”
        teacher (str): 教师姓名

    Examples:
        >>> s = Subject(name='语文', simplified_name='语', teacher='张三')
        >>> s.name
        '语文'
        >>> s.simplified_name
        '语'
        >>> s.teacher
        '张三'
    """
    name: str
    simplified_name: str
    teacher: str


class Lesson(BaseModel):
    """
    单节课程。

    Args:
        subject (Subject): 课程的科目
        start_time (datetime.time): 开始的时间
        end_time (datetime.time): 结束的时间

    Examples:
        >>> l = Lesson(subject=Subject(name='语文', simplified_name='语', teacher='张三'), \
                       start_time=datetime.time(8, 0, 0), end_time=datetime.time(8, 45, 0))
        >>> l.subject.name
        '语文'
        >>> l.start_time
        datetime.time(8, 0)
        >>> l.end_time
        datetime.time(8, 45)
    """
    subject: Subject
    start_time: datetime.time
    end_time: datetime.time


class WeekType(Enum):
    """
    周次类型。
    ALL: 适用于所有周
    ODD: 仅适用于单周
    EVEN: 仅适用于双周
    """
    ALL = "all"
    ODD = "odd"
    EVEN = "even"


class SingleDaySchedule(BaseModel):
    """
    单日课程安排。

    Args:
        enable_day (int): 课程安排的星期（如 1 表示星期一）
        classes (list[Lesson]): 课程列表，每个课程包含科目、开始时间和结束时间
        name (str): 课程安排名称（如 "星期一"）
        weeks (WeekType): 周次类型，指定课程适用于哪些周次

    Examples:
        >>> s = SingleDaySchedule(enable_day=1, classes=[Lesson(subject=Subject(name='语文', \
                                  simplified_name='语', teacher='张三'), start_time=datetime.time(8, 0, 0), \
                                  end_time=datetime.time(8, 45, 0))], name='星期一', weeks=WeekType.ALL)
        >>> s.enable_day
        1
        >>> s.name
        '星期一'
        >>> s.weeks
        <WeekType.ALL: 'all'>
    """
    enable_day: int
    classes: list[Lesson]
    name: str
    weeks: WeekType

    def is_enabled_on_week(self, week: int) -> bool:
        """
        判断课程是否在指定的日期上启用。

        Args:
            week (int): 要检查的周次序号

        Returns:
            bool: 如果课程在指定周上启用，则返回 True；否则返回 False

        Examples:
            >>> s = SingleDaySchedule(enable_day=1, classes=[Lesson(subject=Subject(name='语文', \
                                      simplified_name='语', teacher='张三'), start_time=datetime.time(8, 0, 0), \
                                      end_time=datetime.time(8, 45, 0))], name='星期一', weeks=WeekType.ODD)
            >>> s.is_enabled_on_week(3)
            True
            >>> s.is_enabled_on_week(6)
            False
            >>> s.is_enabled_on_week(11)
            True
        """
        return {
            WeekType.ALL: True,  # 适用于所有周 -> 永久启用
            WeekType.ODD: week % 2 == 1,  # 单周
            WeekType.EVEN: week % 2 == 0  # 双周
        }[self.weeks]

    def is_enabled_on_day(self, start_day: datetime.date, day: datetime.date) -> bool:
        """
        判断课程是否在指定的日期上启用。

        Args:
            day (int): 要检查的日期（1 表示星期一，2 表示星期二，依此类推）
            start_day (datetime.date): 课程开始的日期，用于计算周次

        Returns:
            bool: 如果课程在指定日期上启用，则返回 True；否则返回 False

        Examples:
            # >>> s = SingleDaySchedule(enable_day=1, classes=[Lesson(subject=Subject(name='语文', \
            #                           simplified_name='语', teacher='张三'), start_time=datetime.time(8, 0, 0), \
            #                           end_time=datetime.time(8, 45, 0))], name='星期一', weeks=WeekType.ODD)
            # >>> s.is_enabled_on_day(datetime.date(2025, 9, 1), datetime.date(2025, 9, 4))
            # True
            # >>> s.is_enabled_on_day(datetime.date(2025, 9, 1), datetime.date(2025, 9, 16))
            # True
            # >>> s.is_enabled_on_day(datetime.date(2025, 9, 1), datetime.date(2025, 9, 24))
            # False
        """
        return self.is_enabled_on_week(utils.week_num(start_day, day))
