class FoundToggle:
    def __init__(self, name, fname):
        self.name = name
        self.fname = fname
        self.type = []
        self.alias = []

    def addType(self, type):
        if type not in self.type:
            self.type.append(type)

    def addAlias(self, alias):
        if alias not in self.alias:
            self.alias.append(alias)

