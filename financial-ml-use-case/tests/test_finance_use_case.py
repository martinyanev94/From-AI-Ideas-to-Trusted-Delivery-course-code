from src.finance_use_case import (
    EvidenceClaim,
    FinanceUseCase,
    RiskRegisterEntry,
    RiskTolerance,
    recommendation,
)


def make_use_case(**overrides):
    values = {
        "name": "weekly portfolio shortlist",
        "intended_decision": "prioritize assets for review",
        "decision_owner": "portfolio manager",
        "risk_tolerance": RiskTolerance.CAUTIOUS,
        "explanation_needs": ("factor contribution",),
        "evidence_requirements": ("time-aware validation",),
    }
    values.update(overrides)
    return FinanceUseCase(**values)


def make_risk(**overrides):
    values = {
        "risk": "incorrect ranking contributes to financial loss",
        "consequence": "manager may act on an unsuitable shortlist",
        "control": "advisory output and loss analysis",
        "accountable_owner": "portfolio manager",
        "review_trigger": "material loss pattern",
    }
    values.update(overrides)
    return RiskRegisterEntry(**values)


def test_complete_use_case_validates():
    assert make_use_case().validate() == []


def test_missing_owner_requires_revision():
    assert make_use_case(decision_owner="").validate() == ["decision_owner"]


def test_missing_control_requires_revision():
    assert make_risk(control="").validate() == ["control"]


def test_partial_claim_requires_revision():
    claim = EvidenceClaim("improves review", "partial")
    assert recommendation(make_use_case(), (claim,), make_risk()) == "revise"


def test_empty_claims_require_revision():
    assert recommendation(make_use_case(), (), make_risk()) == "revise"


def test_invalid_status_requires_revision():
    claim = EvidenceClaim("improves review", "verified")
    assert recommendation(make_use_case(), (claim,), make_risk()) == "revise"


def test_supported_bounded_claim_allows_bounded_pilot():
    claim = EvidenceClaim("improves review", "supported")
    assert recommendation(make_use_case(), (claim,), make_risk()) == "bounded_pilot"


def test_missing_risk_control_requires_revision():
    claim = EvidenceClaim("improves review", "supported")
    assert recommendation(make_use_case(), (claim,), make_risk(control="")) == "revise"
