from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path

import scrapdynamics as sd

SAVE_FORMAT = ["json", "csv", "excel"]

def parse_argument() -> Namespace:
    """parse command line arguments

    Returns:
        Namespace: command parsing results
    """
    
    parser = ArgumentParser("ScrapDynamics")
    
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("-u", "--url", type=str, help="base url")
    parser.add_argument("-o", "--output", type=Path, help="path/filename.extention")
    
    return parser.parse_args()

def main():
    """command line entrypoint for direct CLI invocation
    """    
    
    args = parse_argument()
    
    if args.version: print(sd.__version__)
    if not args.url: return
    # get output format
    if args.output:
        output_suffix = args.output.suffix[1:]
        assert len(output_suffix) > 0, "output path should be: path/filename.extention"
        assert output_suffix in SAVE_FORMAT, f"file extention should be one of the following: {SAVE_FORMAT}"
    
    crawler = sd.Crawler(args.url)
    crawler.start()
    print(crawler.show())
    
    if args.output: eval(f"""crawler.to_{output_suffix}(r"{args.output}")""")
    
if __name__ == "__main__":
    main()