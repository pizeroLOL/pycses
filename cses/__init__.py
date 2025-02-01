from dataclasses import dataclass
from datetime import time
from os import PathLike
from typing import Any, List, Literal, Optional

import yaml


def _str_or_none(item: Any) -> Optional[str]:
    return None if item is None else str(item)


@dataclass
class Subject:
    """CSES 科目"""

    name: str
    simplified_name: Optional[str]
    teacher: Optional[str]
    room: Optional[str]

    @staticmethod
    def from_dict(item: dict) -> "Subject":
        """从字典导入"""

        return Subject(
            name=str(item["name"]),
            simplified_name=_str_or_none(item.get("simplified_name")),
            teacher=_str_or_none(item.get("teacher")),
            room=_str_or_none(item.get("room")),
        )

    def export_to_dict(self) -> dict:
        """导出到字典"""

        return self.__dict__


@dataclass
class Class:
    """CSES 课程安排"""

    subject: str
    start_time: time
    end_time: time

    @staticmethod
    def from_dict(item: dict) -> "Class":
        """从字典导入"""

        return Class(
            subject=str(item["subject"]),
            start_time=time.fromisoformat(str(item["start_time"])),
            end_time=time.fromisoformat(str(item["end_time"])),
        )

    def export_to_dict(self) -> dict:
        """导出到字典"""

        return {
            "subject": self.subject,
            "start_time": self.start_time.isoformat("seconds"),
            "end_time": self.end_time.isoformat("seconds"),
        }


Weekday = Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
weekday_items = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WeekType = Literal["all", "odd", "even"]
week_types = ["all", "odd", "even"]


def try_into_enable_day(item: str) -> Weekday:
    """将字符串转换到星期"""
    if item not in weekday_items:
        raise ValueError(f"enable_day 不可为 {item}，应为 {weekday_items}")
    return item  # type: ignore


def try_into_weeks(item: str) -> WeekType:
    """将字符串转换到周类型"""
    if item not in week_types:
        raise ValueError(f"weeks 不可为 {item}，应为 {weekday_items}")
    return item  # type: ignore


@dataclass
class Schedule:
    """CSES 日时间线"""

    name: str
    enable_day: Weekday
    weeks: WeekType
    classes: List[Class]

    @staticmethod
    def from_dict(item: dict) -> "Schedule":
        """从字典导入"""
        return Schedule(
            name=str(item["name"]),
            enable_day=try_into_enable_day(str(item["enable_day"])),
            weeks=try_into_weeks(str(item["weeks"])),
            classes=list(
                Class.from_dict(dict(raw_class))
                for raw_class in list(item.get("classes", list()))
            ),
        )

    def export_to_dict(self) -> dict:
        """导出到字典"""
        temp_output = self.__dict__
        temp_output["classes"] = list(
            class_.export_to_dict() for class_ in self.classes
        )
        return temp_output


@dataclass
class CsesConfig:
    """CSES 配置文件"""

    verison: int
    subjects: List[Subject]
    schedules: List[Schedule]

    @staticmethod
    def load_from_dict(item: dict) -> "CsesConfig":
        return CsesConfig(
            verison=int(item.get("version", 1)),
            subjects=list(
                Subject.from_dict(dict(raw_subject))
                for raw_subject in list(item.get("subjects", list()))
            ),
            schedules=list(
                Schedule.from_dict(dict(raw_schedule))
                for raw_schedule in list(item.get("schedules", list()))
            ),
        )

    @staticmethod
    def read_from_file(path: PathLike) -> "CsesConfig":
        """读取 CSES 文件"""

        def read_yaml(path: PathLike) -> dict:
            with open(path, "r", encoding="utf-8") as i:
                return dict(yaml.safe_load(i))

        raw_config = read_yaml(path)
        return CsesConfig.load_from_dict(raw_config)

    def export_to_dict(self) -> dict:
        """导出到字典"""

        return {
            "version": self.verison,
            "subjects": list(subject.export_to_dict() for subject in self.subjects),
            "schedules": list(schedule.export_to_dict() for schedule in self.schedules),
        }

    def save_to_file(self, path: PathLike):
        """保存文件"""
        with open(path, "w", encoding="utf-8") as o:
            yaml.dump(
                self.export_to_dict(),
                o,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )


if __name__ == "__main__":
    from pathlib import Path
    import sys

    def none_to_str(item: Optional[str]) -> str:
        return "" if item is None else item

    if len(sys.argv) != 2:
        print("""Check CSES File
Usage: python -m cses <cses_file>""")
        sys.exit(1)

    file_path = sys.argv[1]
    parser = CsesConfig.read_from_file(Path(file_path))

    print("All Subjects:")
    for subject in parser.subjects:
        print(f"{subject.name} ({none_to_str(subject.simplified_name)})")
        print(f"- Teacher: {none_to_str(subject.teacher)}")
        print(f"- Room: {none_to_str(subject.room)}")

    print("\nAll Schedules:")
    for schedule in parser.schedules:
        print(f"{schedule.name} ({schedule.enable_day} {schedule.weeks}):")
        for cls in schedule.classes:
            print(f"- {cls.subject} ({cls.start_time} - {cls.end_time})")
    parser.save_to_file(Path("temp.yml"))
