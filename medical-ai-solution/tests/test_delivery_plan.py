from src.delivery_plan import DeliveryPlan, record_feedback, review_due


def make_plan() -> DeliveryPlan:
    return DeliveryPlan(
        clinical_reviewer="Dr. Chen",
        deployment_owner="Priya",
        workflow_owner="Nurse Patel",
        response_owner="Priya",
        feedback_route="clinical-review queue",
        safeguards=["human fallback", "rollback", "stop"],
        review_days=30,
    )


def test_complete_plan_validates():
    assert make_plan().validate() == []


def test_feedback_preserves_route_and_owners():
    feedback = record_feedback(make_plan(), "alert missed recent treatment change")
    assert feedback == {
        "observation": "alert missed recent treatment change",
        "route": "clinical-review queue",
        "reviewer": "Dr. Chen",
        "response_owner": "Priya",
    }


def test_review_is_due_at_interval():
    assert review_due(make_plan(), 30) is True
    assert review_due(make_plan(), 29) is False


def test_missing_stop_control_is_invalid():
    plan = make_plan()
    plan.safeguards.remove("stop")
    assert "stop safeguard required" in plan.validate()
