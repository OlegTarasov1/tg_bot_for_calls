


def get_user_data_text(
    first_name: str,
    last_name: str,
    job_title: str,
    username: str,
    is_admin: bool
) -> str:
    
    data = f"{first_name} {last_name}, {username}\n\n"
    data += f"job title: {job_title}\n\n"
    data += 'admin' if is_admin else 'not an admin'

    return data