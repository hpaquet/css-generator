import re

from css_generator.ruleset.rule import Rule


def get_rule_type(s):
    if s == '#':
        return 'ID'
    elif s == '.':
        return 'CLASS'
    elif s == '@':
        return 'MEDIA'

    return 'ELEMENT'


class StyleParser:

    def __init__(self):
        self.raw_data = ''
        self.raw_rules = None
        self.rules = []

    def from_file(self, path, stylesheet=None):
        with open(path, 'r') as f:
            data = f.read()

        if not stylesheet:
            from css_generator.ruleset.stylesheet import StyleSheet
            stylesheet = StyleSheet()

        self.feed(data)

        stylesheet.add_rules(self.rules)

        self.reset()

        return stylesheet

    def _clean(self, string):
        """Remove comments form string"""
        return re.sub('(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)', '', string.replace('\n', ''))

    def feed(self, data):
        self.raw_data += self._clean(data)

        self.raw_rules = self._parse_stylesheet(self.raw_data)

        for name, values in self.raw_rules.items():
            self.rules += [self._convert_rule(name, values)]

    def reset(self):
        self.raw_data = ''
        self.raw_rules = None
        self.rules = []

    @staticmethod
    def _parse_rule(raw):

        rules = []

        start_rule = None
        rule_type = None
        open_bracket = 0

        i = 0

        for c in raw:

            if (start_rule is None) & (c != '\n'):
                start_rule = i
                rule_type = get_rule_type(c)

            if c == '{':
                open_bracket += 1

            if c == '}':
                if open_bracket == 1:
                    rules += [[rule_type, raw[start_rule:i+1]]]
                    start_rule = None
                    rule_type = None

                open_bracket -= 1

            i += 1

        return rules

    def _parse_stylesheet(self, raw):

        raw_rules = self._parse_rule(raw)
        rules = {}

        for raw_rule in raw_rules:

            selector = re.findall('((.|[\r\n])*?\{)', raw_rule[1])[0][0][:-2].lstrip().rstrip()
            properties = re.findall('(\{(.|[\r\n])*\})', raw_rule[1])[0][0][1:-1].lstrip().rstrip()

            if raw_rule[0] == 'MEDIA':
                properties = self._parse_stylesheet(properties)

            if isinstance(properties, str):
                properties = {v.lstrip().split(':')[0]: v.lstrip().split(':')[1] for v in properties.split(';') if v}

            if selector in rules.keys():
                rules[selector].update(properties)
                continue

            rules[selector] = properties

        return rules

    def _convert_rule(self, name, properties):

        rule_type = get_rule_type(name[0])

        if rule_type == 'MEDIA':
            sub_rules = properties
            properties = []
            for media_rule_name, media_rule_properties in sub_rules.items():
                properties += [self._convert_rule(media_rule_name, media_rule_properties)]

        return Rule(
            rule_selector=name,
            rule_type=type,
            properties=properties
        )
