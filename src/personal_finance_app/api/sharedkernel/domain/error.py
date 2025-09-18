from __future__ import annotations
from dataclasses import dataclass

from personal_finance_app.api.sharedkernel.domain.error_type import ErrorType


@dataclass(frozen=True)
class Error:
    code: str
    description: str
    error_type: ErrorType

    @staticmethod
    def failure(code, description) -> Error:
        return Error(code, description, ErrorType.FAILURE)

    @staticmethod
    def not_found(code, description) -> Error:
        return Error(code, description, ErrorType.NOT_FOUND)

    @staticmethod
    def conflict(code, description) -> Error:
        return Error(code, description, ErrorType.CONFLICT)

    @staticmethod
    def validation(code, description) -> Error:
        return Error(code, description, ErrorType.VALIDATION)
