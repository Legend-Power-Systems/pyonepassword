import re
from enum import Enum


class FieldTypeEnum(Enum):
    PASSWORD = "password"
    TEXT = "text"
    URL = "url"


class _FieldAssignment(str):

    def __new__(cls, field_label: str, value: str, *args, field_type=FieldTypeEnum.PASSWORD, section_label: str = None, **kwargs) -> None:
        assignment_str = ""
        field_label = cls._field_assignment_escape(field_label)
        field_type_string = field_type.value
        if section_label:
            section_label = cls._field_assignment_escape(section_label)
            assignment_str = f"{section_label}."

        assignment_str += f"{field_label}[{field_type_string}]="
        # intentionally not using string formatting to assign value
        # in some cases value will be a RedactedString, so concatenation
        # will prevent it from self-redacting
        assignment_str += value
        return super().__new__(cls, assignment_str)

    @classmethod
    def _field_assignment_escape(cls, input_string):

        pattern = r"([.=\\])"
        repl = r"\\\1"
        escaped_string = re.sub(pattern, repl, input_string)
        return escaped_string


class PasswordFieldAssignment(_FieldAssignment):
    def __new__(cls, field_label: str, value: str, section_label: str = None):
        field_type = FieldTypeEnum.PASSWORD
        obj = super().__new__(cls, field_label, value,
                              field_type=field_type, section_label=section_label)
        return obj

    def __init__(self, *args, **kwargs):
        super().__init__()
        redacted = self._redact()
        self._redacted_assignment = redacted

    def __str__(self):
        return self._redacted_assignment

    def _redact(self):
        lhs, rhs = self.rsplit("=", maxsplit=1)
        mask = "*" * len(rhs)

        # introduce an intentional syntax error here
        # in case we try to use this redacted string as the actual
        # assignment during execution
        # This should generate an error
        # we don't want to accidentaly set someone's password
        # to "*************"
        # this is an equals emoji rather than an equals sign
        redacted = f"{lhs}🟰{mask}"
        return redacted
