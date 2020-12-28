from .rule import Rule


class Media(Rule):
    """Sequence of rules that represent a media query"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = 'media'
