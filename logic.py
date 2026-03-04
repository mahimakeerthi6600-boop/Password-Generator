import random
import string


def generate_password(length, use_numbers=True, use_symbols=True):
    """
    Generate a random password.

    Args:
        length (int): Desired password length (must be >= 4)
        use_numbers (bool): Include digits (0-9)
        use_symbols (bool): Include symbols (!@#$%^&* etc.)

    Returns:
        str: Generated password

    Raises:
        ValueError: If length < 4 or no character set is selected
    """
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    char_pool = string.ascii_letters  # always include letters

    if use_numbers:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("At least one character set must be selected.")

    # Guarantee at least one char from each selected set
    guaranteed = [random.choice(string.ascii_letters)]
    if use_numbers:
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        guaranteed.append(random.choice(string.punctuation))

    remaining = [random.choice(char_pool) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining
    random.shuffle(password_list)
    return "".join(password_list)


def validate_length(value):
    """
    Validate that the given value is a valid password length.

    Args:
        value: The value to validate (string or int)

    Returns:
        int: Parsed integer length

    Raises:
        ValueError: If value is not a positive integer >= 4
    """
    try:
        length = int(value)
    except (ValueError, TypeError):
        raise ValueError("Length must be a whole number.")

    if length < 4:
        raise ValueError("Password length must be at least 4.")
    if length > 128:
        raise ValueError("Password length must not exceed 128.")

    return length


def check_password_strength(password):
    """
    Return a strength label for the given password.

    Returns one of: 'Weak', 'Fair', 'Strong', 'Very Strong'
    """
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 16:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 1:
        return "Weak"
    elif score == 2:
        return "Fair"
    elif score == 3:
        return "Strong"
    else:
        return "Very Strong"