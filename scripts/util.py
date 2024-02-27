import glob

system_root = '../../'
ch_version = '80.0.3946.0'

FileExtensionMap = {
    "GO": ['.go'],
    "CPP": ['.cpp', '.c', '.cc'],
    "PYTHON": ['.py'],
    "JAVASCRIPT": ['.js'],
    "JAVA": ['.java'],
}


def getSwitchFilesGlob(rootPath=system_root, projectName='chromium'):
    return glob.glob(f'{rootPath}/{projectName}/**/*_switches.cc', recursive=True)


def getConfigFilesGlob(rootPath=system_root, projectName='chromium'):
    return glob.glob(f'{rootPath}/{projectName}/**/*.cc', recursive=True)

"""
regx = string[] of regx name, e.g. [r'GetBoolProperty.*%s']
toggleName = string of toggle name
"""
def allRegExpOfToggles(regx, toggleName):
    return [i%toggleName for i in regx]


def getPatternWithToggleName(patterns, toggleName):
    return [p%toggleName for p in patterns]