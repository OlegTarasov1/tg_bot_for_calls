from aiogram.utils.keyboard import InlineKeyboardBuilder 
from models.models import UserBase

def get_employee_view(
    is_admin: bool,
    employee: UserBase
) -> str:
    result = f"{employee.first_name} {employee.last_name}\n"
    result += f"Ник: {employee.username}\n"
    result += f"ID: {employee.id}\n"
    result += f"Должность: {employee.job_title}\n"

    if is_admin:
        result += f"Админ: {'да' if employee.is_admin else 'нет'}\n"
        result += f"Скрам: {'да' if employee.scrum else 'нет'}\n"

    return result