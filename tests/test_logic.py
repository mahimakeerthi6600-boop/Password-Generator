import string
import pytest
from logic import generate_password, validate_length, check_password_strength


# ── generate_password ────────────────────────────────────────────────────────

class TestGeneratePassword:

    def test_correct_length(self):
        pwd = generate_password(12)
        assert len(pwd) == 12

    def test_default_includes_letters(self):
        pwd = generate_password(20)
        assert any(c in string.ascii_letters for c in pwd)

    def test_includes_numbers_when_enabled(self):
        found = False
        for _ in range(20):
            pwd = generate_password(16, use_numbers=True, use_symbols=False)
            if any(c.isdigit() for c in pwd):
                found = True
                break
        assert found

    def test_excludes_numbers_when_disabled(self):
        for _ in range(30):
            pwd = generate_password(16, use_numbers=False, use_symbols=False)
            assert not any(c.isdigit() for c in pwd)

    def test_includes_symbols_when_enabled(self):
        found = False
        for _ in range(20):
            pwd = generate_password(16, use_numbers=False, use_symbols=True)
            if any(c in string.punctuation for c in pwd):
                found = True
                break
        assert found

    def test_excludes_symbols_when_disabled(self):
        for _ in range(30):
            pwd = generate_password(16, use_numbers=False, use_symbols=False)
            assert not any(c in string.punctuation for c in pwd)

    def test_minimum_length_4(self):
        pwd = generate_password(4)
        assert len(pwd) == 4

    def test_length_below_minimum_raises(self):
        with pytest.raises(ValueError):
            generate_password(3)

    def test_length_zero_raises(self):
        with pytest.raises(ValueError):
            generate_password(0)

    def test_large_length(self):
        pwd = generate_password(128)
        assert len(pwd) == 128

    def test_passwords_are_different(self):
        passwords = {generate_password(20) for _ in range(10)}
        assert len(passwords) > 1

    def test_only_letters_when_both_disabled(self):
        for _ in range(20):
            pwd = generate_password(12, use_numbers=False, use_symbols=False)
            assert all(c in string.ascii_letters for c in pwd)


# ── validate_length ──────────────────────────────────────────────────────────

class TestValidateLength:

    def test_valid_integer_string(self):
        assert validate_length("16") == 16

    def test_valid_integer(self):
        assert validate_length(20) == 20

    def test_minimum_boundary(self):
        assert validate_length(4) == 4

    def test_maximum_boundary(self):
        assert validate_length(128) == 128

    def test_below_minimum_raises(self):
        with pytest.raises(ValueError, match="at least 4"):
            validate_length(3)

    def test_above_maximum_raises(self):
        with pytest.raises(ValueError, match="128"):
            validate_length(129)

    def test_non_numeric_string_raises(self):
        with pytest.raises(ValueError):
            validate_length("abc")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            validate_length("")

    def test_float_string_raises(self):
        with pytest.raises(ValueError):
            validate_length("12.5")

    def test_none_raises(self):
        with pytest.raises(ValueError):
            validate_length(None)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            validate_length(-1)


# ── check_password_strength ──────────────────────────────────────────────────

class TestCheckPasswordStrength:

    def test_weak_short_letters_only(self):
        assert check_password_strength("abc") == "Weak"

    def test_weak_medium_letters_only(self):
        assert check_password_strength("abcdefgh") == "Weak"

    def test_fair_letters_and_digit(self):
        assert check_password_strength("abcdefg1") == "Fair"

    def test_strong_with_digit_and_symbol(self):
        assert check_password_strength("abcdef1!") == "Strong"

    def test_very_strong_long_with_digit_and_symbol(self):
        assert check_password_strength("abcdefghijklmnop1!") == "Very Strong"

    def test_all_strength_labels_are_valid(self):
        valid = {"Weak", "Fair", "Strong", "Very Strong"}
        for length in [4, 8, 16, 32]:
            pwd = generate_password(length, use_numbers=True, use_symbols=True)
            assert check_password_strength(pwd) in valid