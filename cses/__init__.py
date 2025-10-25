"""
使用 ``CSES`` 类可以表示、解析一个 CSES 课程文件。
"""
import yaml

import cses.structures as st
import cses.errors as err


class CSES:
    """
    用来表示、解析一个 CSES 课程文件的类。
    """

    def __init__(self, content: str):
        """
        初始化 CSES。

        Args:
            content (str): CSES 课程文件的内容。
        """
        self.schedule = None
        self.version = None

        self._load(content)

    def _load(self, content: str):
        """
        从 ``content`` 加载 CSES 课程文件的内容。

        Args:
            content (str): CSES 课程文件的内容。
        """
        data = yaml.safe_load(content)

        # 版本处理&检查
        self.version = data['version']
        if self.version != 1:
            raise err.VersionError(f'不支持的版本号: {self.version}')

        # 科目处理&检查
        try:
            self.subjects = {s['name']: st.Subject(**s) for s in data['subjects']}
        except st.ValidationError as e:
            raise err.ParseError(f'科目数据有误: {data['subjects']}') from e

        # 课程处理&检查
        schedules = data['schedules']
        try:
            # 先构造课程列表，再构造课表
            schedule_classes = {i['name']: i['classes'] for i in schedules}
            built_lessons = {i['name']: [] for i in schedules}
            for name, classes in schedule_classes.items():
                for lesson in classes:
                    built_lessons[name].append(
                        st.Lesson(**(lesson | {'subject': self.subjects[lesson['subject']]}))
                    )  # 从self.subjects中获取合法的Subject对象

            # 从构造好的课程列表中构造课表
            self.schedule = [
                st.SingleDaySchedule(
                    enable_day=day['enable_day'],
                    classes=built_lessons[day['name']],
                    name=day['name'],
                    weeks=st.WeekType(day['weeks']),
                )
                for day in schedules
            ]

            print("!!!\n", self.schedule)
        except st.ValidationError as e:
            raise err.ParseError(f'课程数据有误: {data['schedules']}') from e

