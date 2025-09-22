# from sqlalchemy.orm import (
#     mapped_column,
#     Mapped
# )
# from sqlalchemy import (
#     BigInteger,
#     String,
#     ForeignKey,
#     or_
# )
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from .base import Base



# class UserBase(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(BigInteger, primary_key = True)

#     first_name: Mapped[str] = mapped_column(String(60), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(60), nullable=False)
#     job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
#     username: Mapped[str] = mapped_column(String(255)) 
#     chat_id: Mapped[int] = mapped_column(BigInteger, nullable = True)

#     employee: Mapped[list["UserBase"]] = relationship(
#         "UserBase",
#         back_populates = "scrum_master",
#         secondary = "user_call_association",
#         primaryjoin = "UserBase.id == UsersCallsAssociation.scrum_master_id",
#         secondaryjoin = "UsersCallsAssociation.employee_id == UserBase.id"
#     )
#     scrum_master: Mapped[list["UserBase"]] = relationship(
#         "UserBase",
#         back_populates="employee",
#         secondary = "user_call_association",
#         primaryjoin = "UserBase.id ==  UsersCallsAssociation.employee_id",
#         secondaryjoin = "UsersCallsAssociation.scrum_master_id == UserBase.id"
#     )
    
#     calls_scrum_masters: Mapped[list["CallsBase"]] = relationship(
#         "CallsBase",
#         back_populates = "scrum_masters",
#         secondary = "user_call_association",
#         primaryjoin = "UserBase.id == UsersCallsAssociation.scrum_master_id",
#         secondaryjoin = "UsersCallsAssociation.call_id == CallsBase.id"
#     )
#     calls_employees: Mapped[list["CallsBase"]] = relationship(
#         "CallsBase",
#         back_populates = "employees",
#         secondary = "user_call_association",
#         primaryjoin = "UserBase.id == UsersCallsAssociation.employee_id",
#         secondaryjoin = "UsersCallsAssociation.call_id == CallsBase.id"
#     )


# class CallsBase(Base):
#     __tablename__ = "calls"

#     id: Mapped[int] = mapped_column(primary_key = True)
#     call_purpouse: Mapped[str] = mapped_column(String(255), default = "созвон")
#     link: Mapped[str]
#     time: Mapped[datetime] = mapped_column(nullable = False)

#     scrum_masters: Mapped[list["UserBase"]] = relationship(
#         "UserBase",
#         back_populates = "calls_scrum_masters",
#         secondary = "user_call_association",
#         primaryjoin = "CallsBase.id == UsersCallsAssociation.call_id",
#         secondaryjoin = "UsersCallsAssociation.scrum_master_id == UserBase.id",
#     )

#     employees: Mapped[list["UserBase"]] = relationship(
#         "UserBase",
#         back_populates= "calls_employees",
#         secondary = "user_call_association",
#         primaryjoin = "CallsBase.id == UsersCallsAssociation.call_id",
#         secondaryjoin = "UsersCallsAssociation.employee_id == UserBase.id",
#     )


# class UsersCallsAssociation(Base):
#     __tablename__ = "user_call_association"

#     id: Mapped[int] = mapped_column(primary_key = True)
#     group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), default = 1)
    
#     employee_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
#     scrum_master_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     call_id: Mapped[int] = mapped_column(ForeignKey("calls.id"))

#     users: Mapped["UserBase"] = relationship(
#         "UsersBase",
#         foreign_keys = [employee_id],
#         back_populates = "user_call_connections"
#     )
#     group: Mapped["GroupsBase"] = relationship(back_populates = "users_and_calls_association")


# class GroupsBase(Base):
#     __tablename__ = "groups"

#     id: Mapped[int] = mapped_column(primary_key = True)
#     group_name: Mapped[str] = mapped_column(String(255))

#     users_and_calls_association: Mapped[list["UsersCallsAssociation"]] = relationship(back_populates = "group")
    
    
# # class UserBase(Base):
# #     __tablename__ = "users"

# #     id: Mapped[int] = mapped_column(BigInteger, primary_key = True)

# #     first_name: Mapped[str] = mapped_column(String(60), nullable=False)
# #     last_name: Mapped[str] = mapped_column(String(60), nullable=False)
# #     job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
# #     username: Mapped[str] = mapped_column(String(255)) 
# #     chat_id: Mapped[int] = mapped_column(BigInteger, nullable = True)

# #     is_admin: Mapped[bool] = mapped_column(default = False)
# #     is_scrum: Mapped[bool | None] = mapped_column(default = False)
# #     is_employee: Mapped[bool] = mapped_column(default = False)
# #     scrum: Mapped[bool | None] = mapped_column(nullable=True, default = False)

# #     user_call_connections: Mapped[list["UsersCallsAssociation"]] = relationship(
# #         "UsersCallsAssociation",
# #         back_populates = "users",
# #         foreign_keys = ["UsersCallsAssociation.employee_id"]
# #     )
# #     calls_scrum_masters: Mapped[list["CallsBase"]] = relationship(
# #         "CallsBase",
# #         back_populates = "scrum_masters",
# #         secondary = "user_call_association",
# #         primaryjoin = "UserBase.id == UsersCallsAssociation.scrum_master_id",
# #         secondaryjoin = "UsersCallsAssociation.call_id == CallsBase.id"
# #     )