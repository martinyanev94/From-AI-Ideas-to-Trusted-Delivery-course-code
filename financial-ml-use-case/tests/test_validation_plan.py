import pytest

from src.validation_plan import Control, ValidationSlice, recommendation, validate_slice


def control() -> Control:
    return Control("review", "owner", "trigger", "response")


def test_revise_when_a_material_slice_needs_evidence() -> None:
    slices = [ValidationSlice("time", "later period", "record", "pass"),
              ValidationSlice("segment", "group", "missing record", "revise")]
    assert recommendation(slices, [control()]) == "revise"


def test_stop_overrides_passing_slices() -> None:
    slices = [ValidationSlice("time", "later period", "record", "pass"),
              ValidationSlice("stress", "adverse case", "breach", "stop")]
    assert recommendation(slices, [control()]) == "stop"


def test_all_pass_and_complete_controls_can_proceed() -> None:
    slices = [ValidationSlice("time", "later period", "record", "pass")]
    assert recommendation(slices, [control()]) == "proceed"


def test_missing_control_response_requires_revision() -> None:
    slices = [ValidationSlice("time", "later period", "record", "pass")]
    incomplete = Control("review", "owner", "trigger", "")
    assert recommendation(slices, [incomplete]) == "revise"


def test_slice_metadata_is_required() -> None:
    with pytest.raises(ValueError):
        validate_slice(ValidationSlice("", "question", "evidence", "pass"))
