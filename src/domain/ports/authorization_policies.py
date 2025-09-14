from src.domain.value_objects.user_role import UserRole


def can_list_users(role: UserRole) -> bool:
    """
    Business policy: only admins can list all users.

    Args:
        role: Role of the caller.

    Returns:
        True if allowed; False otherwise.
    """
    return role == UserRole.ADMIN


def can_read_user(subject_id: int, target_id: int, role: UserRole) -> bool:
    """
    Business policy: a user can read themselves; admins can read anyone.

    Args:
        subject_id: ID of the caller.
        target_id: ID of the user being accessed.
        role: Role of the caller.

    Returns:
        True if reading target is allowed; False otherwise.
    """
    return subject_id == target_id or role == UserRole.ADMIN


def can_modify_user(role: UserRole) -> bool:
    """
    Business policy: only admins can modify other users' data.

    Args:
        role: Role of the caller.

    Returns:
        True if modification is allowed; False otherwise.
    """
    return role == UserRole.ADMIN
