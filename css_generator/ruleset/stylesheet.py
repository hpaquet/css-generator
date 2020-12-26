from collections.abc import MutableSequence

from css_generator.ruleset.rule import Rule
from css_generator import parser


class StyleSheet(MutableSequence):
    """Sequence of rules that represent a stylesheet"""

    def __init__(self, rules=None, *args):
        self.rules = list()
        self.extend(list(args))

    def __getitem__(self, i):
        return self.rules[i]

    def __setitem__(self, i, v):
        if issubclass(v, Rule):
            self.rules[i] = v

    def __delitem__(self, i):
        del self.rules[i]

    def __len__(self):
        return len(self.rules)

    @property
    def type(self):
        return 'text/css'

    def insert(self, i, v):
        if isinstance(v, Rule):
            self.rules.insert(i, v)

    def append(self, v):
        if isinstance(v, Rule):
            self.rules.append(v)

    def add_rules(self, values):
        if values is None:
            return

        elif isinstance(values, list):
            for item in values:
                self.add_rule(item)

    def add_rule(self, rule):
        if isinstance(rule, Rule):
            self.append(rule)

    def css(self, path=None):
        style = ''

        for rule in self.rules:
            style += rule.css()

        if path:
            with open(path, 'w') as f:
                f.write(style)

        return style

    @classmethod
    def from_file(cls, path):

        return parser.from_file(path, stylesheet=cls())


if __name__ == '__main__':
    stylesheet = StyleSheet.from_file(path='style.css')

