# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from utils.sql_connector import CallStatus

# ok_keyboard = InlineKeyboardMarkup(
#     [
#         [InlineKeyboardButton("\U00002705 Ок", callback_data="menu")],
#     ]
# )


# back_keyboard = InlineKeyboardMarkup(
#     [
#         [InlineKeyboardButton("\U000025c0 Назад", callback_data="menu")],
#     ]
# )


# # Меню клавиатура
# def get_menu_keyboard(is_admin: bool = False, is_scrum: bool = False):
#     buttons = [
#         [InlineKeyboardButton("\U0001f4c5 Расписание", callback_data="call_page_1")],
#     ]

#     if is_admin or is_scrum:
#         buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U0001f4d6 Список сотрудников", callback_data="users_page_1"
#                 )
#             ]
#         )
#         buttons.append(
#             [InlineKeyboardButton("\U0001f6b7 Пропуски", callback_data="missed_call")]
#         )
#     if is_scrum:
#         buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U0001f504 Обновить ссылку", callback_data="update_call_link"
#                 )
#             ]
#         )
#     buttons.append(
#         [
#             InlineKeyboardButton(
#                 "\U0000274c Больше не работаю", callback_data="dont_work"
#             )
#         ]
#     )
#     inline_keyboard = InlineKeyboardMarkup(buttons)

#     return inline_keyboard


# # Информация о сотруднике
# def get_employee_view(is_admin: bool, employee) -> str:
#     result = f"{employee.full_name}\n"
#     result += f"Ник: {employee.nickname}\n"
#     result += f"ID: {employee.id}\n"
#     result += f"Должность: {employee.job_title}\n"

#     if is_admin:
#         result += f"Админ: {'да' if employee.is_admin else 'нет'}\n"
#         result += f"Скрам: {'да' if employee.scrum else 'нет'}\n"

#     return result


# # Информация о встрече
# def get_employee_timetable_view(call, is_scrum: bool) -> str:
#     result = f"Звонок с сотрудником {call.employee.full_name}\n"
#     result += f"Проводит {call.scrum.full_name}\n"
#     result += f"Время: {call.datetime.strftime('%d.%m.%Y %H:%M')}\n"
#     result += f"Цель: {call.purpose}\n"
#     if is_scrum:
#         result += f"Ссылка: {call.call_link}\n"
#     if call.status == CallStatus.canceled:
#         result += "Статус: отменён\n"
#     elif call.status == CallStatus.process:
#         result += "Статус: в процессе\n"
#     elif call.status == CallStatus.wait:
#         result += "Статус: ожидание\n"
#     elif call.status == CallStatus.successful:
#         result += "Статус: завершён\n"
#     return result


# # Список сотрудников
# def create_user_list_keyboard(
#     employees, page: int, employees_per_page: int, is_admin: bool = False
# ) -> InlineKeyboardMarkup:
#     page_buttons = [
#         [
#             InlineKeyboardButton(
#                 f"{employee.first_name} {employee.last_name}",
#                 callback_data=f"user_info_{employee.id}",
#             )
#         ]
#         for employee in employees
#     ]

#     nav_buttons = []
#     if page > 1:
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U000025c0 Назад", callback_data=f"users_page_{page - 1}"
#             )
#         )

#     nav_buttons.append(InlineKeyboardButton("\U0001f4d2 Меню", callback_data="menu"))

#     if employees_per_page == len(employees):
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U000025b6 Вперед", callback_data=f"users_page_{page + 1}"
#             )
#         )

#     page_buttons.append(nav_buttons)
#     if is_admin:
#         page_buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U00002795 Добавить сотрудника", callback_data="add_employee"
#                 )
#             ]
#         )

#     inline_keyboard = InlineKeyboardMarkup(page_buttons)
#     return inline_keyboard


# # Расписание встреч
# def create_call_list_keyboard(
#     page: int, calls_per_page: int, calendar, is_scrum: bool = False
# ) -> InlineKeyboardMarkup:
#     page_buttons = []
#     for call in calendar:
#         status_symbol = ""
#         if call.status == CallStatus.wait:
#             status_symbol = "\U000023f3"  # ⏳
#         elif call.status == CallStatus.process:
#             status_symbol = "\U0001f5e3"  # 🗣
#         elif call.status == CallStatus.successful:
#             status_symbol = "\U00002705"  # ✅
#         elif call.status == CallStatus.canceled:
#             status_symbol = "\U0000274c"  # ❌
#         page_buttons.append(
#             [
#                 InlineKeyboardButton(
#                     f"{status_symbol} {call.datetime.strftime('%H:%M')} |\t{call.employee.full_name}\n",
#                     callback_data=f"call_info_{call.call_id}",
#                 )
#             ]
#         )

#     page_buttons.sort(key=lambda x: x[0].text.split("\n")[1])

#     nav_buttons = []
#     if page > 1:
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U000025c0 Назад", callback_data=f"call_page_{page - 1}"
#             )
#         )

#     nav_buttons.append(InlineKeyboardButton("\U0001f4d2 Меню", callback_data="menu"))
#     if is_scrum:
#         nav_buttons.append(
#             InlineKeyboardButton("\U000023e9 Сдвиг", callback_data="shift_calls")
#         )

#     if calls_per_page == len(calendar):
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U000025b6 Вперед", callback_data=f"call_page_{page + 1}"
#             )
#         )

#     # Конечный вид кнопок
#     page_buttons.append(nav_buttons)

#     inline_keyboard = InlineKeyboardMarkup(page_buttons)
#     return inline_keyboard


# # Информация о сотруднике
# def create_user_info_keyboard(is_admin: bool, user_id: int):
#     page_buttons = []
#     nav_buttons = []
#     nav_buttons.append(
#         InlineKeyboardButton("\U000025c0 Назад", callback_data="users_page_1")
#     )
#     if is_admin:
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U0000274c Удалить", callback_data=f"delete_user_{user_id}"
#             )
#         )
#         page_buttons.append(nav_buttons)
#         page_buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U0001f504 Обновить", callback_data=f"update_user_{user_id}"
#                 )
#             ]
#         )
#         page_buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U0001f4dd Ответы с последней встречи",
#                     callback_data=f"answer_list_{user_id}",
#                 )
#             ]
#         )
#         page_buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U0001f4e2 Позвать на встречу",
#                     callback_data=f"invite_user_{user_id}",
#                 )
#             ]
#         )
#     else:
#         page_buttons.append(nav_buttons)
#     inline_keyboard = InlineKeyboardMarkup(page_buttons)
#     return inline_keyboard


# # Информация о встрече
# def create_call_info_keyboard(
#     is_scrum: bool,
#     is_admin: bool,
#     call_id: str,
#     call_status: CallStatus,
#     call_link: str,
# ):
#     page_buttons = []
#     nav_buttons = []
#     if call_status == CallStatus.wait:
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U000023e9 Перенести", callback_data=f"move_time_{call_id}"
#             )
#         )
#         nav_buttons.append(
#             InlineKeyboardButton(
#                 "\U0000274c Отклонить", callback_data=f"cancel_call_{call_id}"
#             )
#         )
#         nav_buttons.append(
#             InlineKeyboardButton("\U0000260e Принять", callback_data="menu")
#         )
#     else:
#         nav_buttons.append(
#             InlineKeyboardButton("\U000025c0 Назад", callback_data="menu")
#         )

#     if is_admin or is_scrum:
#         if call_status == CallStatus.wait:
#             page_buttons.append(nav_buttons)
#             page_buttons.append(
#                 [
#                     InlineKeyboardButton(
#                         "\U00002705 Начать", callback_data=f"start_call_{call_id}"
#                     ),
#                 ]
#             )
#         elif call_status == CallStatus.process:
#             page_buttons.append(nav_buttons)
#             page_buttons.append(
#                 [InlineKeyboardButton("\U0001f517 Открыть", url=call_link)]
#             )
#             page_buttons.append(
#                 [
#                     InlineKeyboardButton(
#                         "\U0000260e Завершить", callback_data=f"success_call_{call_id}"
#                     ),
#                 ]
#             )
#         page_buttons.append(
#             [
#                 InlineKeyboardButton(
#                     "\U0001f504 Обновить цель",
#                     callback_data=f"update_purpose_call_{call_id}",
#                 )
#             ]
#         )
#     else:
#         page_buttons.append(nav_buttons)
#     inline_keyboard = InlineKeyboardMarkup(page_buttons)
#     return inline_keyboard


# # После начала конференции
# # User
# def create_starting_keyboard(
#     call_link: int, call_id: int, questions_count: int, random_question_id: int
# ):
#     buttons = [
#         [InlineKeyboardButton("\U0001f517 Открыть", url=call_link)],
#         [
#             InlineKeyboardButton(
#                 "\U0000260e Завершить", callback_data=f"success_call_{call_id}"
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 "Рандомный вопрос",
#                 callback_data=f"random_question_{random_question_id}_{call_id}",
#             )
#         ],
#     ] + [
#         [InlineKeyboardButton(f"Анкета {i}", callback_data=f"question_{i}_{call_id}")]
#         for i in range(1, questions_count + 1)
#     ]
#     inline_keyboard = InlineKeyboardMarkup(buttons)
#     return inline_keyboard


# # После начала конференции
# # Scrum
# def create_starting_scrum_keyboard(call_link: int, call_id: int, questions_count: int):
#     buttons = [
#         [InlineKeyboardButton("\U0001f517 Открыть", url=call_link)],
#         [
#             InlineKeyboardButton(
#                 "\U0000260e Обновить цель",
#                 callback_data=f"update_purpose_call_{call_id}",
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 "\U0000260e Завершить", callback_data=f"success_call_{call_id}"
#             )
#         ],
#     ] + [
#         [
#             InlineKeyboardButton(
#                 f"Анкета {i}", callback_data=f"scrum_question_{i}_{call_id}"
#             )
#         ]
#         for i in range(1, questions_count + 1)
#     ]
#     inline_keyboard = InlineKeyboardMarkup(buttons)
#     return inline_keyboard


# # Еженедельная анкета
# def create_friday_keyboard(questions_count):
#     buttons = [
#         [InlineKeyboardButton(f"Анкета {i}", callback_data=f"friday_question_{i}")]
#         for i in range(1, questions_count + 1)
#     ]
#     inline_keyboard = InlineKeyboardMarkup(buttons)
#     return inline_keyboard


# # Клавиатура для просмотра ответов
# def get_answers_list(answers, user_id):
#     page_buttons = [
#         [
#             InlineKeyboardButton(
#                 f"Анкета №{answer.question_id}",
#                 callback_data=f"question_num_{answer.question_id}_{user_id}",
#             )
#         ]
#         for answer in answers
#     ]
#     page_buttons.append(
#         [
#             InlineKeyboardButton(
#                 "Рандомный вопрос",
#                 callback_data=f"question_num_{0}_{user_id}",
#             )
#         ]
#     )

#     page_buttons.append(
#         [
#             InlineKeyboardButton(
#                 "Назад",
#                 callback_data=f"user_info_{user_id}",
#             )
#         ]
#     )
#     inline_keyboard = InlineKeyboardMarkup(page_buttons)
#     return inline_keyboard


# def get_missed_call_keyboard(calls):
#     page_buttons = [
#         [
#             InlineKeyboardButton(
#                 f"{call.calendar.datetime.strftime('%d/%m/%Y, %H:%M')} {call.calendar.employee.full_name}",
#                 callback_data=f"missed_call_id_{call.call_id}",
#             )
#         ]
#         for call in calls
#     ]
#     page_buttons.append(
#         [InlineKeyboardButton("\U000025c0 Назад", callback_data="menu")]
#     )
#     inline_keyboard = InlineKeyboardMarkup(page_buttons)
#     return inline_keyboard
