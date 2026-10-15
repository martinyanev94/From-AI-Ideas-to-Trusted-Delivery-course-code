from suitability import NLPProposal, assess


proposal = NLPProposal(
    name="support urgency routing",
    intended_outcome="flag messages for faster human urgent review",
    input_description="customer message text plus queue metadata",
    ambiguity_examples=(
        "sarcasm can resemble urgency",
        "indirect requests may omit the actual problem",
        "short messages may lack necessary context",
    ),
    evidence_requirements=(
        "representative labeled messages from relevant support channels",
        "a held-out evaluation set with urgent and routine cases",
        "review of false positives and false negatives by support leads",
    ),
    risks=(
        "a missed urgent message may delay human attention",
        "uneven language coverage may route some customers less reliably",
    ),
    non_goals=(
        "diagnose a customer",
        "send an unsupervised response",
        "decide compensation",
    ),
    human_review_required=True,
)

print(assess(proposal))
