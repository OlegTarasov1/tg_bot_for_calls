from os import getenv
from dotenv import load_dotenv
from sqlalchemy import (
    BOOLEAN,
    String,
    TIMESTAMP,
    TIME,
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
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    Mapped,
    mapped_column,
    declarative_base
)
from datetime import datetime, time
from pytz import timezone 
from .base import Base

# Base = declarative_base()

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

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    scrum: Mapped[bool] = mapped_column(nullable=False, default=False)

    inactive_periods = relationship("InactiveEmployee", back_populates="employee")
    calendar_entries = relationship("Calendar", foreign_keys="[Calendar.employee_id]", back_populates="employee")
    scrum_entries = relationship("Calendar", foreign_keys="[Calendar.scrum_id]", back_populates="scrum")
    default_calendar_entries = relationship("DefaultCalendar", foreign_keys="[DefaultCalendar.employee_id]", back_populates="employee")
    default_scrum_entries = relationship("DefaultCalendar", foreign_keys="[DefaultCalendar.scrum_id]", back_populates="scrum")
    friday_forms = relationship("FridayForm", back_populates="employee")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return "{0.full_name}\t\t{0.nickname}".format(self)

class InactiveEmployee(Base):
    __tablename__ = "inactive_employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employee.id"), nullable=False)
    start_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    reason: Mapped[str] = mapped_column(Text)

    employee = relationship("Employee", back_populates="inactive_periods")

class Calendar(Base):
    __tablename__ = "calendar"

    call_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employee.id"), nullable=False)
    scrum_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employee.id"), nullable=False)
    purpose: Mapped[str] = mapped_column(Text)
    call_link: Mapped[str] = mapped_column(Text)
    notified: Mapped[NotifiedStatus] = mapped_column(
        Enum(NotifiedStatus, name="notified_status", create_type=False),
        default=NotifiedStatus.wait,
        nullable=False,
    )
    status: Mapped[CallStatus] = mapped_column(
        Enum(CallStatus, name="call_status", create_type=False),
        default=CallStatus.wait,
        nullable=False,
    )

    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="calendar_entries")
    scrum = relationship("Employee", foreign_keys=[scrum_id], back_populates="scrum_entries")
    missed_calls = relationship("MissedCall", back_populates="calendar")
    daily_forms = relationship("DailyForm", back_populates="calendar")
    scrum_forms = relationship("ScrumForm", back_populates="calendar")
    random_forms = relationship("RandomForm", back_populates="calendar")

    def __repr__(self):
        return (
            "ID: {0.call_id}, "
            + "время: {0.datetime}, "
            + "сотрудник: {0.employee.full_name}, "
            + "скрам: {0.scrum.full_name}"
        ).format(self)

class DefaultCalendar(Base):
    __tablename__ = "default_calendar"

    call_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_time: Mapped[datetime.time] = mapped_column(TIME(timezone=True), nullable=False)
    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employee.id"), nullable=False)
    scrum_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employee.id"), nullable=False)

    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="default_calendar_entries")
    scrum = relationship("Employee", foreign_keys=[scrum_id], back_populates="default_scrum_entries")

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[int] = mapped_column(Integer, ForeignKey("calendar.call_id"), nullable=False)
    reason: Mapped[str] = mapped_column(Text)

    calendar = relationship("Calendar", back_populates="missed_calls")

    def __repr__(self):
        return ("{0.calendar} {0.reason}").format(self)

class RandomQuestion(Base):
    __tablename__ = "random_question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)

    random_forms = relationship("RandomForm", back_populates="question")

    def __repr__(self):
        return self.question

class DailyQuestion(Base):
    __tablename__ = "daily_question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)

    daily_forms = relationship("DailyForm", back_populates="question")

    def __repr__(self):
        return self.question

class ScrumQuestion(Base):
    __tablename__ = "scrum_question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)

    scrum_forms = relationship("ScrumForm", back_populates="question")

    def __repr__(self):
        return self.question

class FridayQuestion(Base):
    __tablename__ = "friday_question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)

    friday_forms = relationship("FridayForm", back_populates="question")

    def __repr__(self):
        return self.question

class DailyForm(Base):
    __tablename__ = "daily_form"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[int] = mapped_column(Integer, ForeignKey("calendar.call_id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("daily_question.id"), nullable=False)
    answer: Mapped[str] = mapped_column(Text)

    question = relationship("DailyQuestion", back_populates="daily_forms")
    calendar = relationship("Calendar", back_populates="daily_forms")

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employee.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("friday_question.id"), nullable=False)
    answer: Mapped[str] = mapped_column(Text)

    question = relationship("FridayQuestion", back_populates="friday_forms")
    employee = relationship("Employee", back_populates="friday_forms")

class ScrumForm(Base):
    __tablename__ = "scrum_form"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[int] = mapped_column(Integer, ForeignKey("calendar.call_id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("scrum_question.id"), nullable=False)
    answer: Mapped[str] = mapped_column(Text)

    question = relationship("ScrumQuestion", back_populates="scrum_forms")
    calendar = relationship("Calendar", back_populates="scrum_forms")

class RandomForm(Base):
    __tablename__ = "random_form"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[int] = mapped_column(Integer, ForeignKey("calendar.call_id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("random_question.id"))
    answer: Mapped[str] = mapped_column(Text)

    question = relationship("RandomQuestion", back_populates="random_forms")
    calendar = relationship("Calendar", back_populates="random_forms")

    def __repr__(self):
        return (
            "<{0.__class__.__name__}"
            + "(ID={0.id!r}, "
            + "call_id={0.call_id!r}, "
            + "question_id={0.question_id!r}, "
            + "answer={0.answer!r})>"
        ).format(self)