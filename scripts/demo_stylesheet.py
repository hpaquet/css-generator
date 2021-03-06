from css_generator import StyleSheet
from css_generator import Rule

stylesheet = StyleSheet()

container = Rule(
    rule_selector='container',
    rule_type='class',
    properties={
        'position': 'relative',
        'width': '100 %',
        'max-width': '960 px',
        'margin': '0 auto',
        'padding': '0 20 px',
        'box-sizing': 'border-box'
    }
)

stylesheet.add_rule(container)
