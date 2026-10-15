import json

from explainability_review import build_requirements, render_report


if __name__ == "__main__":
    print(json.dumps(render_report(build_requirements()), indent=2))
