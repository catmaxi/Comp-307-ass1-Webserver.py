import argparse

parser = argparse.ArgumentParser(
    description='Example with nonoptional arguments',
)

parser.add_argument('IP', action="store")
parser.add_argument('port', action="store")
parser.add_argument('path', action="store")

args = parser.parse_args()
print(args)