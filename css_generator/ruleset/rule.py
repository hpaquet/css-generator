from collections.abc import MutableSequence

from css_generator.ruleset.property import Property
from css_generator.enums import RuleTypes

RIGHT_CURLY_BRAKET = "\u007D"
LEFT_CURLY_BRAKET = "\u007B"
NEW_LINE = "\n"
TAB = "\t"


class Rule(MutableSequence):
    """Sequence of rules that represent a stylesheet"""

    def __init__(self, properties=None, rule_selector=None, rule_type=None, pseudo_class=None, *args):
        self.properties = list()
        self.extend(list(args))
        self.type = rule_type
        self.selector = rule_selector
        self.pseudo_class = pseudo_class

        self.add_properties(properties)

    def __getitem__(self, i):
        return self.properties[i]

    def __setitem__(self, i, v):
        if issubclass(v, Property):
            self.properties[i] = v

    def __delitem__(self, i):
        del self.properties[i]

    def __len__(self):
        return len(self.properties)

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, selector):
        if not isinstance(selector, list):
            selector = [selector]
        self._selector = selector

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def pseudo_class(self):
        return self._pseudo_class

    @pseudo_class.setter
    def pseudo_class(self, pseudo_class):
        if pseudo_class:
            self._pseudo_class = ['', pseudo_class]
        else:
            self._pseudo_class = []

    def insert(self, i, v):
        if isinstance(v, Property) | isinstance(v, Rule):
            self.properties.insert(i, v)

    def append(self, v):
        if isinstance(v, Property) | isinstance(v, Rule):
            self.properties.append(v)

    def add_properties(self, values):
        if values is None:
            return

        elif isinstance(values, dict):
            for k, v in values.items():
                self.add_property({'name': k, 'value': v})

        elif isinstance(values, list):
            for item in values:
                self.add_property(item)

    def add_property(self, property):
        if isinstance(property, dict):
            return self.append(Property(name=property['name'], value=property['value']))

        elif isinstance(property, Property) | isinstance(property, Rule):
            self.append(property)

    def css(self):
        style = ''

        style += ', \n'.join([f"{getattr(RuleTypes, self.type.upper()).value}{s}{':'.join(self.pseudo_class)}" for s in self.selector])
        style += f" {LEFT_CURLY_BRAKET} {NEW_LINE}"

        for property in self.properties:
            if isinstance(property, Property):
                style += TAB + f"{property.name}: {property.value};" + NEW_LINE
            elif isinstance(property, Rule):
                style += TAB
                style += property.css().replace(NEW_LINE, NEW_LINE + TAB)
                style += TAB + NEW_LINE

        style += RIGHT_CURLY_BRAKET

        return style


if __name__ == '__main__':
    container = Rule(
        rule_selector='container',
        rule_type='class',
        properties={
            'width': '85%',
            'padding': '0',
        }
    )

    a_hover = Rule(
        rule_selector='a',
        pseudo_class='hover',
        rule_type='element',
        properties={
            'color': '#0FA0CE',
        }
    )

    rule = Rule(
        rule_selector='(min-width: 400px)',
        rule_type='media',
        properties=[
            container,
            a_hover
        ]
    )

    print(rule.css())
