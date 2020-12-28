from collections.abc import MutableSequence

from css_generator import parser
from css_generator.ruleset.rule import Rule
from css_generator.ruleset.media import Media


def get_media(rule):
    media_index = []
    for i, property in enumerate(rule.properties):
        if isinstance(property, Media):
            media_index.append(i)

    return media_index


class StyleSheet(MutableSequence):
    """Sequence of rules that represent a stylesheet"""

    def __init__(self, rules=None, *args):
        self.rules = list()
        self.extend(list(args))

        self.media_index = []

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
        if isinstance(v, Rule) | isinstance(v, Media):
            self.rules.insert(i, v)

    def append(self, v):
        if isinstance(v, Rule) | isinstance(v, Media):
            self.rules.append(v)

        # return index
        return len(self.rules) - 1

    def add_rules(self, values):
        if values is None:
            return

        elif isinstance(values, list):
            for item in values:
                self.add_rule(item)

    def add_rule(self, rule):
        if isinstance(rule, Rule):
            media_index = get_media(rule)
            media_index.reverse()

            for i in media_index:
                self.add_media(rule.properties[i], parent_rule=rule)
                rule.properties.remove(rule.properties[i])

            self.append(rule)

    def add_media(self, media, parent_rule):
        rule = Rule(
            rule_selector=parent_rule.selector,
            rule_type=parent_rule.type,
            properties=media.properties
        )

        for i in self.media_index:
            if media.selector == self.rules[i].selector:
                self.rules[i].add_properties(rule)
                return

        media = Media(
            rule_selector=media.selector,
            rule_type='media',
            properties=[rule]
        )

        self.media_index.append(self.append(media))

    def css(self, path=None):
        style = ''
        media_style = ''

        for rule in self.rules:
            if isinstance(rule, Media):
                media_style += rule.css()
                continue

            style += rule.css()

        style += media_style

        if path:
            with open(path, 'w') as f:
                f.write(style)

        return style

    @classmethod
    def from_file(cls, path):

        return parser.from_file(path, stylesheet=cls())


if __name__ == '__main__':
    stylesheet = StyleSheet.from_file(path='style.css')

