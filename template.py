import sys

class Injectable(object):
    def __init__(self, is_injectable, template_filename=''):
        self.is_injectable = is_injectable
        self.template_filename = template_filename


FIRST_OPEN_CURLY = 0
IGNORED_CHARACTER = 1
TEMPLATE_FILENAME = 2
FIRST_CLOSE_CURLY = 3


def injectable(line: str) -> Injectable:
    state = IGNORED_CHARACTER
    i = 0

    filename = ''

    while True:
        if state == IGNORED_CHARACTER:
            if line[i] == ' ' or line[i] == '\t' or line[i] == '\n':
                state = IGNORED_CHARACTER
                i += 1
            elif line[i] == '{':
                state = FIRST_OPEN_CURLY
                i += 1
            else:
                return Injectable(False)

        elif state == FIRST_OPEN_CURLY:
            if line[i] == '{':
                state = TEMPLATE_FILENAME
                i += 1
            else:
                return Injectable(False)
        elif state == TEMPLATE_FILENAME:
            if line[i] == ' ':
                i += 1
            elif line[i].isalpha() or line[i] == '/' or line[i] == '.':
                filename += line[i]
                i += 1
            elif line[i] == '}':
                state = FIRST_CLOSE_CURLY
                i += 1
            else:
                return Injectable(False)
        elif state == FIRST_CLOSE_CURLY:
            if line[i] == '}':
                return Injectable(True, filename)
            else:
                return Injectable(False)


def template(input: str, output: str):
    final = ''
    template = ''

    with open(input, 'r') as f:
        lines = f.readlines()

        for line in lines:
            inject = injectable(line)
            if inject.is_injectable:
                with open('src/' + inject.template_filename, 'r') as ff:
                    replacement = ff.read()
                    template = line.replace(line, replacement)

                final += template
            else:
                final += line

    with open(output, 'w') as f:
        f.write(final)

if __name__ == '__main__':
	template(sys.argv[1], sys.argv[2])
