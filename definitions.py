from typing import Dict, List, Tuple


def get_column_expression(entity: str, name: str, definition: Dict[str,dict]) -> str:
    col_funcs = get_column_type, get_column_nullability, get_column_description
    col_items = [func(name, definition) for func in col_funcs if func(name, definition)]

    if name == 'id':
        return  f"{name} = Column({get_column_type(name, definition)}, key='{entity}_id', primary_key=True, name='id')"
    else:
        return f"{name} = Column({', '.join(col_items)})"


def get_column_type(name: str, definition: Dict[str,dict]) -> str:

    prop = definition['properties'][name]
    if prop:
        t, f = prop['type'], prop.get('format')
        if t == 'number':
            if f == 'int32' :
                return 'Integer'
            elif f == 'int64':
                return 'BigInteger'
            elif f == 'double':
                return 'Double'
            else:
                return 'Float'
        elif t == 'string':
            if f == 'datetime':
                return 'DateTime'
            elif f == 'uuid':
                return 'UUID'
            else:
                if 'maxLength' in prop:
                    return f"String{prop['maxLength']}"
                else:
                    return 'String'
        elif t == 'boolean':
            return 'Boolean'


def get_column_nullability(name: str, definition: Dict[str,dict]) -> str:
    return 'nullable=True' if name in definition.get('required') else ''


def get_column_description(name: str, definition: Dict[str,dict]) -> str:
    prop = definition.get(name)
    if prop:
        return f"doc={prop['description']}" if 'description' in prop else ''

