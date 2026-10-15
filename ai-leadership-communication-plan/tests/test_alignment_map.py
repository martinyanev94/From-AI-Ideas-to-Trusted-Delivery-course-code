import pytest

from src.alignment_map import StakeholderRecord, build_map, unresolved_objections


def test_build_map_validates_and_preserves_records():
    record = StakeholderRecord(
        name="Maya",
        role="executive sponsor",
        stated_need="measurable time reduction",
        hidden_incentive="visible AI progress",
        objection="pilot may miss quarterly target",
        influence_paths=("finance review",),
        communication_owner="program lead",
    )

    result = build_map([record])

    assert result == [record]
    assert unresolved_objections(result) == ["Maya"]


def test_blank_influence_path_is_rejected():
    record = StakeholderRecord(
        name="Luis",
        role="operations lead",
        stated_need="trusted workflow",
        hidden_incentive="protect team reliability",
        objection="recommendations may disrupt work",
        influence_paths=("",),
        communication_owner="operations partner",
    )

    with pytest.raises(ValueError, match="influence paths cannot be blank"):
        build_map([record])


def test_missing_influence_path_is_rejected():
    record = StakeholderRecord(
        name="Priya",
        role="data owner",
        stated_need="approved data use",
        hidden_incentive="retain data control",
        objection="request history may be misused",
        influence_paths=(),
        communication_owner="data steward",
    )

    with pytest.raises(ValueError, match="at least one influence path"):
        build_map([record])
