import argparse
import yaml
from definitions import *
import inflect
import stringcase

parser = argparse.ArgumentParser(description='generate SqlAlchemy models form swagger file.')
parser.add_argument('file', type=str, nargs=1,
                    help='File path to parse')

args = parser.parse_args()

p = inflect.engine()


with open(args.file[0]) as file:
    swagger = yaml.load(file, Loader=yaml.FullLoader)
    if 'definitions' in swagger:
        for entity, definition in swagger.get('definitions').items():
            title = definition['title']
            print(f'class {stringcase.pascalcase(title)}(db.Model):\n')
            print(f"    __tablename__ = '{p.plural(title)}'\n")
            for item in definition['properties']:
                print('   ', get_column_expression(definition['title'], item, definition))
            print()

