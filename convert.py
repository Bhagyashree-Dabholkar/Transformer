import sys, json, yaml, argparse
from pathlib import Path

def load_file(path: Path):
    text = path.read_text()
    
    try:
        return json.loads(text), 'json'
    except json.JSONDecodeError:
        pass

    try:
        return yaml.safe_load(text), 'yaml'
    except yaml.YAMLError:
        pass

    raise ValueError(f"File '{path}' is neither valid JSON nor YAML.")

def dump_file(data, out_path: Path, to_yaml: bool):
    text = yaml.dump(data, sort_keys=False) if to_yaml else json.dumps(data, indent=2)
    out_path.write_text(text)

def main():
    parser = argparse.ArgumentParser(description="Convert between JSON & YAML")
    parser.add_argument('input', type=Path, help="Path to input .json/.yaml file")
    parser.add_argument('output', type=Path, help="Desired output file (.json or .yaml/.yml)")

    args = parser.parse_args()
    data, fmt = load_file(args.input)

    to_yaml = args.output.suffix in ('.yaml', '.yml')
    if fmt == 'json' and to_yaml:
        print(f"Converting JSON → YAML")
    elif fmt == 'yaml' and not to_yaml:
        print(f"Converting YAML → JSON")
    elif fmt == 'json' and not to_yaml or fmt == 'yaml' and to_yaml:
        print(f"No format change: output will be {fmt.upper()}")
    dump_file(data, args.output, to_yaml)

if __name__ == '__main__':
    main()
