from pathlib import Path


YEAR = "2024"
DAY = "25"


# Create directory
dir_path = Path(f"./{YEAR}/day{DAY}")
try:
    dir_path.mkdir(parents=True)
    print(f"Directory {dir_path} created.")
except FileExistsError as e:
    print(f"Directory {dir_path} already exists.")


# Create python file
py_file_path = dir_path / f"day{DAY}.py"
if py_file_path.is_file():
    print(f"Python file {py_file_path} already exists.")
else:
    with open(py_file_path, 'w') as f:
        pass
    print(f"Python file {py_file_path} created.")


# Create example file
eg_file_path = dir_path / "example.in"
if eg_file_path.is_file():
    print(f"Example file {eg_file_path} already exists.")
else:
    with open(eg_file_path, 'w') as f:
        pass
    print(f"Example file {eg_file_path} created.")


# Create input file
in_file_path = dir_path / "input.in"
if in_file_path.is_file():
    print(f"Input file {in_file_path} already exists.")
else:
    with open(in_file_path, 'w') as f:
        pass
    print(f"Input file {in_file_path} created.")

# Create question file
qn_file_path = dir_path / "question.txt"
if qn_file_path.is_file():
    print(f"Question file {qn_file_path} already exists.")
else:
    with open(qn_file_path, 'w') as f:
        pass
    print(f"Question file {qn_file_path} created.")
