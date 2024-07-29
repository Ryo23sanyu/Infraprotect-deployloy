def flatten_dict_list(dict_list):
    flat_list = []
    for item in dict_list:
        if isinstance(item, dict):
            flat_list.extend(flatten_dict_list(item.values()))
        elif isinstance(item, list):
            flat_list.extend(flatten_dict_list(item))
        else:
            flat_list.append(item)
    return flat_list

nested_dict_list = [
    {'name': 'Alice', 'details': {'age': 30, 'city': 'Wonderland'}},
    {'name': 'Bob', 'details': {'age': 25, 'city': 'Builderland'}}
]

flat_list = flatten_dict_list(nested_dict_list)
print(flat_list)