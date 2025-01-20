# Toggle Smell Detector
Feature toggle is an worst type of technical debt. There are unknown number of toggle usage patterns created by developers in different source code since there is no standard usage patterns. We identified six usage patterns in Google Chromium in a preliminary study. Although, we are not certain yet which toggle usage patterns are to be called as toggle smells, this project is offering a tool to detect toggle usage patterns in different source code.

Following are the usage patterns our tool can detect as of now.

Dead usage patterns
Nested usage patterns
Spread usage patterns
Mixed usage patterns
Enumeration usage patterns
Combinatorial usage patterns -- Invalid


## Features

- **Supported languages**: Python, Java, C++, C, Go, C#.
- **Patterns detected**: `dead`, `spread`, `nested`, `mixed`, `enum`.
- **Auto-detects programming language**: Automatically identifies the language based on file extension or content.
- **Config paths as relative paths**: Configuration files are provided as paths relative to the source directory.

## Usage

### Basic Syntax
1. Clone the repository:
https://github.com/tajmilur-rahman/toggle-smells.git
2. CD into ts-detector in commandline

3.`` 
python tsd.py -p <source_path> -c <config_paths> [-o <output_path>] [-t <toggle_usage_pattern>] [-l <language>]
``

### Required Arguments

- `-p, --source-path`: Path to the source code directory.
- `-c, --config-path`: Relative paths (from `source-path`) to the configuration files used in the analysis.

### Optional Arguments

- `-o, --output`: Path to save the output JSON file. If not provided, the result will be printed to the console.
- `-t, --toggle-usage`: Specify which toggle usage pattern to detect. If not provided, the script will detect all patterns. Options are:
  - `dead`
  - `spread`
  - `nested`
  - `mixed` (applicable for C++, C, and C#)
  - `enum`
- `-l, --language`: Specify the programming language. If not provided, the script will attempt to auto-detect the language based on file extensions or content.

### Example Usage

#### Example 1: Detect `nested` usage in a C++ project and print output to the console

`python tsd.py -p /path/to/source/ -c src/module/Toggles.cpp src/module/Features.cpp -t nested
`
This command will:
- Use `/path/to/source/` as the source path.
- Check the `src/module/Toggles.cpp` and `src/module/Features.cpp` configuration files (relative to the source path).
- Detect only the `nested` pattern in C++ files.
- Print the results to the console.

#### Example 2: Detect all toggle usage patterns and write output to a file

`python tsd.py -p /path/to/source/ -c src/module/Toggles.cpp src/module/Features.cpp -o outputs/output.json
`

This command will:
- Detect all toggle usage patterns (`dead`, `spread`, `nested`, `mixed`, `enum`).
- Save the results in `outputs/output.json`.

#### Example 3: Manually specify the programming language

`python tsd.py -p /path/to/source/ -c src/module/Toggles.cpp src/module/Features.cpp -l python -o outputs/python-output.json
`

This command will:
- Force the detection to assume Python as the language.
- Save the results to `outputs/python-output.json`.

## Supported Languages

- Python
- Java
- C++
- C
- Go
- C#

If the language is not provided via the `-l` flag, the script will attempt to auto-detect the language based on file extensions or content analysis.

## Output

The result will be a JSON object, either printed to the console or saved to a file. The format will be similar to:

```json
{
  "dead": {
    "toggles": [
      "TOGGLE_1",
      "TOGGLE_2",
      "TOGGLE_3"
    ],
    "qty": 3
  },
  "spread": {
    "toggles": [
      "TOGGLE_3",
      "TOGGLE_4",
      "TOGGLE_5",
      "TOGGLE_6",
      "TOGGLE_7"
    ],
    "qty": 5
  },
  "nested": {
    "toggles": [
      "TOGGLE_1",
      "TOGGLE_6"
    ],
    "qty": 2
  },
  "enum": {
    "toggles": [],
    "qty": 0
  },
  "mixed": {
    "toggles": ["TOGGLE_6"],
    "qty": 1
  }
}
```
In this example:

dead: 3 toggles are identified as dead.
spread: 5 toggles are found to be spread across the code.
nested: 2 toggles are identified as being nested.
enum: No enum toggles were detected.
mixed: 1 toggles are identified as being mixed.


# Sample commands with known repo

[OpenSearch](https://github.com/opensearch-project/OpenSearch): `python tsd.py -p H:\Repos\OpenSearch\ -c server\src\main\java\org\opensearch\common\util\FeatureFlags.java server\src\main\java\org\opensearch\common\settings\FeatureFlagSettings.java`

[SDB2](https://github.com/mathisdt/sdb2/tree/master): `python tsd.py -p H:\Repos\sdb2 -c src\main\java\org\zephyrsoft\sdb2\Feature.java`

[Sentry](https://github.com/getsentry/sentry): `python tsd.py -p H:\Repos\toggle-smells\repos\sentry\ -c src\sentry\conf\server.py src\sentry\features\temporary.py src\sentry\features\permanent.py`

[Pytorch](https://github.com/pytorch/pytorch): `python tsd.py -p H:\Repos\pytorch -c torch\fx\proxy.py `

[Temporal](https://github.com/temporalio/temporal): `python tsd.py -p H:\Repos\temporal -c common\dynamicconfig\constants.go `

[Candence](https://github.com/uber/cadence): `python tsd.py -p H:\Repos\cadence -c common\dynamicconfig\constants.go `

[Vstest](https://github.com/microsoft/vstest): `python tsd.py -p H:\Repos\vstest\ -c src\Microsoft.TestPlatform.CoreUtilities\FeatureFlag\FeatureFlag.cs`

[Bitwarden/Server](https://github.com/bitwarden/server): `python tsd.py -p H:\Repos\server -c src\Core\Constants.cs `

[chromium](https://github.com/chromium/chromium): `python tsd.py -p H:\Repos\chromium -c chrome\browser\flag_descriptions.cc `

[Dawn](https://github.com/google/dawn): `python tsd.py -p H:\Repos\toggle-smells\repos\dawn\ -c src\dawn\native\Toggles.cpp  src\dawn\native\Features.cpp`

# Video Demonstration
https://drive.google.com/file/d/1vlVJeFr0PYZszajo40foBDO8QRNWkLaM/view?usp=drive_link
