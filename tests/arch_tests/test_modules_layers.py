import os
import pytest
from pytestarch import get_evaluable_architecture, Rule

PROJECT_ROOT = os.path.abspath(os.getcwd())
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "src", "personal_finance_app")


@pytest.fixture(scope="module")
def evaluable_architecture():
    return get_evaluable_architecture(root_path=PROJECT_ROOT, module_path=SOURCE_ROOT)


def test_sharedkernel_should_not_import_other_modules(evaluable_architecture):

    rule = (
        Rule()
        .modules_that()
        .are_sub_modules_of(
            "personal-finance-app.src.personal_finance_app.api.sharedkernel"
        )
        .should_not()
        .import_modules_except_modules_that()
        .are_sub_modules_of(
            "personal-finance-app.src.personal_finance_app.api.sharedkernel"
        )
    )

    rule.assert_applies(evaluable_architecture)
