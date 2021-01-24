class CheckStringException(Exception):
    pass


class CheckString:
    field = ""
    pattern_empty_field_error = "Поле с {} должно содержать минимум 1 символ"
    pattern_space_include_error = "Поле с {} не должно содерджать пробельный символ"

    @classmethod
    def check_string(cls, string):
        if not len(string):
            raise CheckStringException(cls.pattern_empty_field_error.format(cls.field))
        if ''.join(string.split(maxsplit=1)) != string:
            raise CheckStringException(cls.pattern_space_include_error.format(cls.field))
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

    @classmethod
    def check_string(cls, string):
        super(CheckPassword, cls).check_string(string)
        if len(string) < 6:
            raise CheckStringException(cls.pattern_empty_field_error.format(cls.field))
        return string


def to_bool(data):
    return bool(int(data))


def id_list(data):
    result = list()

    for i in data:
        if not isinstance(i, int):
            try:
                i = int(i)
            except:
                raise ValueError("Not int")
        result.append(i)

    return result


def is_more_zero(data):
    data = int(float(data))

    if data < 0:
        raise ValueError("Less Zero")
    return data
