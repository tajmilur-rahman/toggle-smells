from scripts.util import *
import glob
from scripts.all_toggle_files import *
# prefix = ["\s(\w*) = \"opensearch\.experimental\..*\.enabled"]
prefix = [
    # r"\s(\w*) = \"opensearch\.experimental\..*\.enabled",
    r'\s(\w*) = Setting\.boolSetting\('
]
project_name = 'opensearch'
allFiles = glob.glob(f'{system_root}/{project_name}/**/**.java', recursive=True)
allFiles = list(filter(lambda path: 'test' not in path and 'qa' not in path, allFiles))

toggles = get_toggles_new(allFiles, prefix)

#combination
combine_pattern = [r'(%s)((\n|.?){0,1}(&&))', r'&&\n\s*(%s)', r'\n\s*&&\s*(%s)']


def getCombineToggles(toggles):
    for file in allFiles:
        with open(file, 'r') as f:
            file_content = f.read()
            for toggle in toggles:
                patterns = allRegExpOfToggles(combine_pattern, toggle.name)
                for pattern in patterns:
                    matches = re.findall(pattern, file_content)
                    if len(matches) > 0:
                        print(toggle.name)
                        print(file)
                    for match in matches:
                        if match is None:
                            continue
                        toggle.addUseInFile(file)

            f.close()

getCombineToggles(toggles)
# for file in allFiles:
#     with open(file, 'rb') as f:
#         for t in toggles:
#             ps = getPatternWithToggleName(combine_pattern, toggles)



# mixed
# java evaluate following as complie time toggle:
# private static final boolean enable = false;
#
# if (enable) {
#   // This will not be included at compile time
# }

