from typing import Tuple, List, Any

from app.constants import FILTER_MARGINS


def validate_filters(fields: List[str], *filter_args: List[str]) -> List[Tuple[str, str]]:
    """Construct a list of valid filter tuples (field, value) from a list of valid fields and user input."""
    filters = []  # NOTE (v_f) v_f

    # print(f'Debug (v_f): len(args): {len(filter_args)}')
    # print(f'Debug (v_f): filter_args: {filter_args}')
    for i in range(0, len(filter_args), 2):
        try:
            # print(f'Debug (v_f): Trying filter construction {i}...')
            field = filter_args[i]
            value = filter_args[i+1]
            # print(f'Debug (v_f): Field: {field}, value: {value}')
            if any(field in fil[0] for fil in filters):
                print('Warning: Cannot have more than 1 filter per field!')
                print(f'Info: denied filter: ({field}, {value})')
                continue
            elif field in fields:
                filters.append((field, value))
                # print(f'Debug (v_f): Added to filters, filters is now: {filters}')
            else:
                print(f'Debug (v_f): invalid field {field}')
        except IndexError as e:
            print(f'Debug (v_f): filter construction failed during iteration {i}.')
            print(f'Debug (v_f): remaining args: {filter_args}')
            print(f'Debug (v_f): {e}')
            break
    return filters


def _filter(items: List[Any], filters: List[Tuple[str, str]]) -> Tuple[List[Any], List[Any]]:
    """Apply a sequence of filters on a sequence of objects, return the exact- and close matches"""
    # 1. exact matches: iteratively filter out the intersection of all items and the matches
    exact_matches = set(items)
    for field, value in filters:
        exact_matches &= {item for item in items if getattr(item, field) == value}

    # 2. close matches:
    #       partial matches (matches that only match some fields)
    #       marginal matches (fields with margin match within it)
    # 2.1. Get ALL matches against the items not included in `exact matches`
    all_close_matches = []
    remaining_items = list(set(items) - exact_matches)
    for field, value in filters:
        if isinstance(FILTER_MARGINS[field], str):
            all_close_matches += [item for item in remaining_items if getattr(item, field) == value]
        else:
            all_close_matches += [item for item in remaining_items
                                  if abs(int(getattr(item, field)) - int(value)) <= FILTER_MARGINS[field]]
    # 2.2. Sort by match count
    match_count = {}
    for item in set(all_close_matches):
        match_count[all_close_matches.count(item)] = item
    close_matches = [v for k, v in sorted(match_count.items(), key=lambda item: item[0])]

    return exact_matches, close_matches  # NOTE actually `close_matches` is a list of str, not a list of Any


def stringify_filter_results(header: str, exact_result: List[Any], close_result: List[Any]) -> str:
    """Creates and returns a nice display format string for the results from a `_filter` call"""
    line = '\n' + '---' * 30 + '\n'
    weak_line = '\n' + '-  ' * 30 + '\n'
    if exact_result:
        exact_text = '\n'.join(str(item) for item in (exact_result))
    else:
        exact_text = f'{"< no exact matches >":^80}'
    if close_result:
        close_text = '\n'.join(str(item) for item in (close_result))
    else:
        close_text = f'{"< no close matches >":^80}'
    return line + header + weak_line + exact_text + weak_line + close_text + line
