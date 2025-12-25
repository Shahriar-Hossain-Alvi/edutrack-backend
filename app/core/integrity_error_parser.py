import re


def parse_integrity_error(error_msg: str) -> str:
    """
    Parse/Extract readable message from PostgreSQL IntegrityError
    example: 'Key (registration)=(213313316) already exists' 
    output: 'Registration 213313316 already exists'
    """
    # constraint name check
    if "students_registration_key" in error_msg:
        # get the value using Regex
        match = re.search(r"Key \(registration\)=\((.*?)\)", error_msg)
        val = match.group(1) if match else ""
        return f"Registration number '{val}' already exists in our records."

    if "users_username_key" in error_msg or "users_email_key" in error_msg:
        return "An account with this email/username already exists."

    if "students_user_id_key" in error_msg:
        return "This user is already assigned to another student profile."

    # If no constraint name found
    return "This record already exists or violates a database constraint."
