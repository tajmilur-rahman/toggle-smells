class FoundToggle:
    def __init__(self, name, fname):
        self.name = name
        self.fname = fname
        self.type = []
        self.alias = [] # => goes to validation in paper, should not be doing, not detecting at the moment
        self.useInFile = []

    def addType(self, type):
        if type not in self.type:
            self.type.append(type)

    def addAlias(self, alias):
        if alias not in self.alias:
            self.alias.append(alias)

    def addUseInFile(self, useInFile):
        if useInFile not in self.useInFile:
            self.useInFile.append(useInFile)