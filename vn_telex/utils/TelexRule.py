class TelexRule:
    def __init__(self, base, modifier, result, kmn_clogic=None, kmn_ologic=None):
        self.base = base
        self.modifier = modifier
        self.result = result
        self.kmn_clogic = kmn_clogic  # Context logic
        self.kmn_ologic = kmn_ologic  # Output logic
