from brief import Brief


brief = Brief(
    context="Routing delays are affecting support operations.",
    evidence="Historical analysis found a 22% reduction in median assignment time.",
    limitations="The sample covers one region and historical tickets.",
    decision="revise",
    action="Run a two-week regional pilot; review urgent-ticket misrouting daily.",
)

print(brief.render())
