from os import getenv

from dotenv import load_dotenv
from sqlalchemy import (
    BOOLEAN,
    String,
    TIMESTAMP,
    TIME,
    VARCHAR,
    BigInteger,
    Column,
    Enum,
    ForeignKey,
    Integer,
    Text,
    create_engine,
    insert,
)
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    Mapped,
    mapped_column
)
from datetime import datetime, timedelta
from pytz import timezone

Base = declarative_base()

class NotifiedStatus(enum.Enum):
    wait = "wait"
    notified = "notified"
    linked = "linked"


class CallStatus(enum.Enum):
    wait = "wait"
    process = "process"
    successful = "successful"
    canceled = "canceled"


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str] = mapped_column(String(60), nullable = False)
    last_name: Mapped[str] = mapped_column(String(60), nullable = False)
    nickname: Mapped[str] = mapped_column(String(255), nullable = False)
    job_title: Mapped[str] = mapped_column(String(255), nullable = True)
    is_admin: Mapped[bool] = mapped_column(default = False)
    scrum: Mapped[bool] = mapped_column(nullable = False, default = False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return "{0.full_name}\t\t{0.nickname}".format(self)


class InactiveEmployee(Base):
    __tablename__ = "inactive_employee"

    id = Column(Integer, primary_key=True)
    employee_id = Column(BigInteger, ForeignKey(Employee.id), nullable=False)
    start_datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    end_datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    reason = Column(Text)

    employee = relationship(Employee, foreign_keys=employee_id)


class Calendar(Base):
    __tablename__ = "calendar"

    call_id = Column(Integer, primary_key=True)
    datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    employee_id = Column(BigInteger, ForeignKey(Employee.id), nullable=False)
    scrum_id = Column(BigInteger, ForeignKey(Employee.id), nullable=False)
    purpose = Column(Text)
    call_link = Column(Text)
    notified = Column(
        Enum(
            NotifiedStatus,
            name="notified_status",
            create_type=False,
        ),
        default=NotifiedStatus.wait,
        nullable=False,
    )
    status = Column(
        Enum(
            CallStatus,
            name="call_status",
            create_type=False,
        ),
        default=CallStatus.wait,
        nullable=False,
    )

    employee = relationship(Employee, foreign_keys=employee_id)
    scrum = relationship(Employee, foreign_keys=scrum_id)

    def __repr__(self):
        return (
            "ID: {0.call_id}, "
            + "время: {0.datetime}, "
            + "сотрудник: {0.employee.full_name}, "
            + "скрам: {0.scrum.full_name}"
        ).format(self)


class DefaultCalendar(Base):
    __tablename__ = "default_calendar"

    call_id = Column(Integer, primary_key=True)
    call_time = Column(TIME(timezone=True), nullable=False)
    employee_id = Column(BigInteger, ForeignKey(Employee.id), nullable=False)
    scrum_id = Column(BigInteger, ForeignKey(Employee.id), nullable=False)

    employee = relationship(Employee, foreign_keys=employee_id)
    scrum = relationship(Employee, foreign_keys=scrum_id)

    def __repr__(self):
        return (
            "<{0.__class__.__name__}"
            + "(call_id={0.call_id!r}, "
            + "time={0.call_time!r}, "
            + "employee={0.employee!r}, "
            + "scrum={0.scrum!r})>"
        ).format(self)


class MissedCall(Base):
    __tablename__ = "missed_call"

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey(Calendar.call_id), nullable=False)
    reason = Column(Text)

    calendar = relationship(Calendar, foreign_keys=call_id)

    def __repr__(self):
        return ("{0.calendar} {0.reason}").format(self)


class RandomQuestion(Base):
    __tablename__ = "random_question"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)

    def __repr__(self):
        return self.question


class DailyQuestion(Base):
    __tablename__ = "daily_question"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)

    def __repr__(self):
        return self.question


class ScrumQuestion(Base):
    __tablename__ = "scrum_question"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)

    def __repr__(self):
        return self.question


class FridayQuestion(Base):
    __tablename__ = "friday_question"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)

    def __repr__(self):
        return self.question


class DailyForm(Base):
    __tablename__ = "daily_form"

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey(Calendar.call_id), nullable=False)
    question_id = Column(Integer, ForeignKey(DailyQuestion.id), nullable=False)
    answer = Column(Text)

    question = relationship(DailyQuestion, foreign_keys=question_id)
    calendar = relationship(Calendar, foreign_keys=call_id)

    def __repr__(self):
        return (
            "<{0.__class__.__name__}"
            + "(ID={0.id!r}, "
            + "call_id={0.call_id!r}, "
            + "question_id={0.question_id!r}, "
            + "answer={0.answer!r})>"
        ).format(self)


class FridayForm(Base):
    __tablename__ = "friday_form"

    id = Column(Integer, primary_key=True)
    datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    question_id = Column(Integer, ForeignKey(FridayQuestion.id), nullable=False)
    answer = Column(Text)

    question = relationship(FridayQuestion, foreign_keys=question_id)
    employee = relationship(Employee, foreign_keys=employee_id)


class ScrumForm(Base):
    __tablename__ = "scrum_form"

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey(Calendar.call_id), nullable=False)
    question_id = Column(Integer, ForeignKey(ScrumQuestion.id), nullable=False)
    answer = Column(Text)

    question = relationship(ScrumQuestion, foreign_keys=question_id)
    calendar = relationship(Calendar, foreign_keys=call_id)


class RandomForm(Base):
    __tablename__ = "random_form"

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey(Calendar.call_id), nullable=False)
    question_id = Column(Integer, ForeignKey(RandomQuestion.id))
    answer = Column(Text)

    question = relationship(RandomQuestion, foreign_keys=question_id)
    calendar = relationship(Calendar, foreign_keys=call_id)

    def __repr__(self):
        return (
            "<{0.__class__.__name__}"
            + "(ID={0.id!r}, "
            + "call_id={0.call_id!r}, "
            + "question_id={0.question_id!r}, "
            + "answer={0.answer!r})>"
        ).format(self)

