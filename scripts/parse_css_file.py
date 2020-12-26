from css_generator.ruleset.stylesheet import StyleSheet
from css_generator.parser import parser

stylesheet = StyleSheet()

style = parser.from_file(path='style.css', stylesheet=stylesheet)