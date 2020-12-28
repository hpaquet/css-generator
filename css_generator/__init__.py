from css_generator._version import __version__

from css_generator.styleparser import StyleParser

parser = StyleParser()

from css_generator.ruleset.stylesheet import StyleSheet
from css_generator.ruleset.rule import Rule
from css_generator.ruleset.media import Media
from css_generator.ruleset.property import Property
