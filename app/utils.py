class Whitespace(object):
    line = '\n' + '---' * 30 + '\n'
    weak_line = '\n' + '-  ' * 30 + '\n'
    clear = 50 * '\n'

    @staticmethod
    def big_title(titletext: str) -> str:
        """Generate a fancy title spacer, the titletext must be less than 40 characters."""
        if len(titletext) > 40:
            print(f'Warning: titletext larger than 40 charachters!\n{titletext}')
            titletext = 'Invalid title, stupid.'
        line = f'>{"-"*50}<'
        space = f'>{" "*50}<'
        delta, remainder = divmod((50 - len(titletext)), 2)
        fill1 = '' if remainder < 1 else ' '
        fill2 = '' if remainder < 2 else ' '
        title = f'>{" "*delta}{fill1}{titletext}{fill2}{" "*delta}<'
        return '\n'.join('{:^80}'.format(s) for s in [line, space, title, space, line])


def str_sized(string: str, lenth: int, end: str = ' ') -> str:
    """Cuts off a long string to conform with `lenth`, replace the end of the string with `end` if provided.

    Args:
        string (str): the string to format
        lenth (int): the max lenth of the string
        end (str): replace the end of the cut string with `end`

    Returns:
        str: the formatted string
    """
    lenth -= len(end)
    if lenth <= 0 or len(string) <= lenth:
        return string
    else:
        return string[:lenth] + end
