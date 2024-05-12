from os import environ


class TokenParser:
    def __init__(self, config_file=None):
        self.tokens = {}
        self.config_file = config_file

    def parse_from_env(self):
        self.tokens = dict(
            (c + 1, t)
            for c, (_, t) in enumerate(
                filter(
                    lambda n: n[0].startswith(
                        "MULTI_TOKEN"), sorted(environ.items())
                )
            )
        )
        return self.tokens
