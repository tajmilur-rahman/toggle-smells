import glob


system_root = '../../'
ch_version = '80.0.3946.0'

def getSwitchFilesGlob(rootPath=system_root, projectName='chromium'):
    return glob.glob(f'{rootPath}/{projectName}/**/*_switches.cc', recursive=True)


def getConfigFilesGlob(rootPath=system_root, projectName='chromium'):
    return glob.glob(f'{rootPath}/{projectName}/**/*.cc', recursive=True)



