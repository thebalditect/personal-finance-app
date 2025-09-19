import os
import pytest
from pytestarch import Rule, get_evaluable_architecture

PROJECT_ROOT = os.path.abspath(os.getcwd())
SOURCE_ROOT = os.path.join(
    PROJECT_ROOT, "src", "personal_finance_app", "api", "sharedkernel"
)


@pytest.fixture(scope="module")
def evaluable_arch():
    return get_evaluable_architecture(PROJECT_ROOT, SOURCE_ROOT)


def test_domain_should_not_depend_on_other_modules(evaluable_arch):

    unallowed_modules = [
        "personal-finance-app.src.personal_finance_app.api.sharedkernel.infrastructure",
        "personal-finance-app.src.personal_finance_app.api.sharedkernel.application",
    ]

    rule = (
        Rule()
        .modules_that()
        .are_named(
            "personal-finance-app.src.personal_finance_app.api.sharedkernel.domain"
        )
        .should_not()
        .import_modules_that()
        .are_named(unallowed_modules)
    )

    rule.assert_applies(evaluable_arch)


def test_application_module_should_not_depend_on_infrastructure_module(evaluable_arch):

    unallowed_modules = [
        "personal-finance-app.src.personal_finance_app.api.sharedkernel.infrastructure",
    ]

    rule = (
        Rule()
        .modules_that()
        .are_named(
            "personal-finance-app.src.personal_finance_app.api.sharedkernel.application"
        )
        .should_not()
        .import_modules_that()
        .are_named(unallowed_modules)
    )

    rule.assert_applies(evaluable_arch)
