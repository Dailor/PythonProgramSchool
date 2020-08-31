class CheckString:
    field = ""
    pattern_empty_field_error = "Поле с {} должно содержать минимум 1 символ"
    pattern_space_include_error = "Поле с {} не должно содерджать пробельный символ"

    def check_string(self, string):
        if not len(string):
            raise ValueError(self.pattern_empty_field_error.format(self.field))
        if ''.join(string.split(maxsplit=1)) != string:
            raise ValueError(self.pattern_space_include_error.format(self.field))
        return string


class CheckName(CheckString):
    field = "именем"


class CheckSurname(CheckString):
    field = "фамилией"


class CheckEmail(CheckString):
    field = 'почтой'


class CheckPassword(CheckString):
    field = "паролем"
    pattern_empty_field_error = "Поле с {} должно содержать минимум 6 символов"

    def check_string(self, string):
        super(CheckPassword, self).check_string(string)
        if len(string) < 6:
            raise ValueError(self.pattern_empty_field_error.format(self.field))
        return string