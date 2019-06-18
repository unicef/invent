from typing import Dict, List, Tuple, Union


def remove_keys(data_dict: Dict, keys: Union[List, Tuple]) -> Dict:
    for key in keys:
        if key in data_dict:
            data_dict.pop(key, None)
    return data_dict
