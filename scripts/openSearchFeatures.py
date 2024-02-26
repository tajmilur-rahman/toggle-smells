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

toggles = get_toggles_new(allFiles, prefix)
for i in toggles:
    print(i.name)

#combination
combine_pattern = [r'%s((\n|.?)*(&&))']
getPatternWithToggleName(combine_pattern, toggles[0].name)

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

