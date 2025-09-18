from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, List, Union

from personal_finance_app.api.sharedkernel.domain.error import Error

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    value: Optional[T]
    errors: Optional[List[T]]

    @property
    def is_success(self) -> bool:
        return self.errors is None or len(self.errors) == 0

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @staticmethod
    def success(value: T) -> Result[T]:
        return Result(value, errors=[])

    @staticmethod
    def failure(errors: Union[Error, List[Error]]) -> Result[T]:

        if isinstance(errors, Error):
            errors = [errors]
        return Result(value=None, errors=errors)
