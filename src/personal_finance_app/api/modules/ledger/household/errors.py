from personal_finance_app.api.sharedkernel.domain.error import Error
from personal_finance_app.api.sharedkernel.domain.error_type import ErrorType


class HouseholdErrors:
    ERROR_CODE = "Ledger.Household.ValidationError"

    @classmethod
    def invalid_name(cls) -> Error:
        return Error(
            code=cls.ERROR_CODE,
            description="name cannot be empty or whitespace.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def invalid_description(cls) -> Error:
        return Error(
            code=cls.ERROR_CODE,
            description="description cannot be empty or whitespace.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def invalid_email(cls) -> Error:
        return Error(
            code=cls.ERROR_CODE,
            description="email should be of format abc@example.com.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def invalid_gender(cls) -> Error:
        Error(
            code=cls.ERROR_CODE,
            description="gender should not be empty or just whitespace.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def invalid_image_format(cls) -> Error:
        return Error(
            code=cls.ERROR_CODE,
            description="avatar should be a valid png.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def unborn_member(cls):
        return Error(
            code=cls.ERROR_CODE,
            description="birth date cannot be in future.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def member_younger_than_sixteen_years_of_age(cls):
        return Error(
            code=cls.ERROR_CODE,
            description="member should be at least sixteen years old as on today.",
            error_type=ErrorType.VALIDATION,
        )

    @classmethod
    def member_already_added_to_household(cls, email: str):
        return Error(
            code=cls.ERROR_CODE,
            description=f"Member with {email} is already a member of the household.",
            error_type=ErrorType.VALIDATION,
        )
