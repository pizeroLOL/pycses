"""使用 ``CSES`` 类可以表示、解析一个 CSES 课程文件。"""
import yaml

import cses.structures as st
import cses.errors as err


class CSES:
    """
    用来表示、解析一个 CSES 课程文件的类。

    该类有如下属性：
        - ``schedule``: 课程安排列表，每个元素是一个 ``SingleDaySchedule`` 对象。
        - ``version``: 课程文件的版本号。目前只能为 ``1`` ，参见 CSES 官方文档与 Schema 文件。
        - ``subjects``: 科目列表，每个元素是一个 ``Subject`` 对象。

    Examples:
        >>> c = CSES.from_file('../cses_example.yaml')
        >>> c.version  # 只会为 1
        1
        >>> c.subjects  # doctest: +NORMALIZE_WHITESPACE
        {'数学': Subject(name='数学', simplified_name='数', teacher='李梅', room='101'),
         '语文': Subject(name='语文', simplified_name='语', teacher='王芳', room='102'),
         '英语': Subject(name='英语', simplified_name='英', teacher='张伟', room='103'),
         '物理': Subject(name='物理', simplified_name='物', teacher='赵军', room='104')}

    """

    def __init__(self):
        """
        新建一个空CSES课表。

        .. warning:: 不应该直接调用 ``CSES()`` 构造函数， 而是应该使用 ``CSES.from_str()`` 工厂方法。
        """
        self.schedule = None
        self.version = None
        self.subjects = None

    @classmethod
    def from_str(cls, content: str) -> 'CSES':
        """
        从 ``content`` 新建一个 CSES 课表对象。

        Args:
            content (str): CSES 课程文件的内容。
        """
        data = yaml.safe_load(content)
        new_schedule = cls()

        # 版本处理&检查
        new_schedule.version = data['version']
        if new_schedule.version != 1:
            raise err.VersionError(f'不支持的版本号: {new_schedule.version}')

        # 科目处理&检查
        try:
            new_schedule.subjects = {s['name']: st.Subject(**s) for s in data['subjects']}
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
                        st.Lesson(**(lesson | {'subject': new_schedule.subjects[lesson['subject']]}))
                    )  # 从self.subjects中获取合法的Subject对象

            # 从构造好的课程列表中构造课表
            new_schedule.schedule = [
                st.SingleDaySchedule(
                    enable_day=day['enable_day'],
                    classes=built_lessons[day['name']],
                    name=day['name'],
                    weeks=st.WeekType(day['weeks']),
                )
                for day in schedules
            ]
        except st.ValidationError as e:
            raise err.ParseError(f'课程数据有误: {data['schedules']}') from e

        return new_schedule

    @classmethod
    def from_file(cls, fp: str) -> 'CSES':
        """
        从路径 ``fp`` 中读取并新建一个 CSES 课表对象。

        Args:
            fp (str): CSES 课程文件的路径。
        """
        with open(fp, encoding='utf8') as f:
            return CSES.from_str(f.read())
