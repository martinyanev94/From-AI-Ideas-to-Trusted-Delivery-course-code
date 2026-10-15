import argparse
from portfolio import load_items, render_dashboard

def main() -> None:
    parser = argparse.ArgumentParser(description="Render a portfolio review dashboard")
    parser.add_argument("--input", default="data/portfolio.json")
    args = parser.parse_args()
    print(render_dashboard(load_items(args.input)))

if __name__ == "__main__":
    main()
