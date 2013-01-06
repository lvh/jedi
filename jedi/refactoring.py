""" Introduce refactoring """

import api
import modules
import difflib
import helpers


class Refactoring(object):
    def __init__(self, change_dct):
        """
        :param change_dct: dict(old_path=(new_path, old_lines, new_lines))
        """
        self.change_dct = change_dct

    def old_files(self):
        dct = {}
        for old_path, (new_path, old_l, new_l) in self.change_dct.items():
            dct[new_path] = '\n'.join(new_l)
        return dct

    def new_files(self):
        dct = {}
        for old_path, (new_path, old_l, new_l) in self.change_dct.items():
            dct[new_path] = '\n'.join(new_l)
        return dct

    def diff(self):
        texts = []
        for old_path, (new_path, old_l, new_l) in self.change_dct.items():
            print old_path, new_path, old_l, new_l
            if old_path:
                udiff = difflib.unified_diff(old_l, new_l)
            else:
                udiff = difflib.unified_diff(old_l, new_l, old_path, new_path)
            texts.append('\n'.join(udiff))
        return '\n'.join(texts)


def rename(new_name, source, *args, **kwargs):
    """ The `args` / `kwargs` params are the same as in `api.Script`.
    :param operation: The refactoring operation to execute.
    :type operation: str
    :type source: str
    :return: list of changed lines/changed files
    """
    dct = {}
    def process(path, old_lines, new_lines):
        if new_lines is not None:  # goto next file, save last
            dct[path] = path, old_lines, new_lines

    script = api.Script(source, *args, **kwargs)
    old_names = script.related_names()
    order = sorted(old_names, key=lambda x: (x.module_path, x.start_pos),
                            reverse=True)

    current_path = object()
    new_lines = old_lines = None
    for name in order:
        if name.in_builtin_module():
            continue
        if current_path != name.module_path:
            current_path = name.module_path

            process(current_path, old_lines, new_lines)
            if current_path is not None:
                # None means take the source that is a normal param.
                with open(current_path) as f:
                    source = f.read()

            new_lines = modules.source_to_unicode(source).splitlines()
            old_lines = new_lines[:]

        nr, indent = name.start_pos
        line = new_lines[nr - 1]
        new_lines[nr - 1] = line[:indent] + new_name + \
                            line[indent + len(name.name_part):]

    process(current_path, old_lines, new_lines)
    return Refactoring(dct)


def extract(new_name, source, *args, **kwargs):
    """ The `args` / `kwargs` params are the same as in `api.Script`.
    :param operation: The refactoring operation to execute.
    :type operation: str
    :type source: str
    :return: list of changed lines/changed files
    """
    new_lines = modules.source_to_unicode(source).splitlines()
    old_lines = new_lines[:]

    script = api.Script(source, *args, **kwargs)
    user_stmt = script._parser.user_stmt

    # TODO care for multiline extracts
    dct = {}
    if user_stmt:
        indent = user_stmt.start_pos[0]
        pos = script.pos
        line_index = pos[0] - 1
        import parsing
        assert isinstance(user_stmt, parsing.Statement)
        call, index, stop = helpers.scan_array_for_pos(
                                        user_stmt.get_assignment_calls(), pos)
        assert isinstance(call, parsing.Call)
        exe = call.execution
        if exe:
            s = exe.start_pos[0], exe.start_pos[1] + 1
            positions = [s] + call.execution.arr_el_pos + [exe.end_pos]
            start_pos = positions[index]
            end_pos = positions[index + 1][0], positions[index + 1][1] - 1
            print start_pos, end_pos
            text = new_lines[start_pos[0] - 1][start_pos[1]:end_pos[1]]
            print text
            for l in range(start_pos[0], end_pos[0] - 1):
                text
            new_lines[start_pos[0]:end_pos[0]-1]
            text = user_stmt.start_pos[1], user_stmt.end_pos[1]
            new = "%s%s = %s" % (' ' * indent, new_name, text)
            new_lines.insert(line_index, new)
    dct[script.source_path] = script.source_path, old_lines, new_lines
    return Refactoring(dct)