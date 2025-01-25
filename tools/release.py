import re
import os
import sys
from datetime import date

import tomlkit as toml
import changelog
from semver import Version


with open("version") as f:
    old_version = Version.parse(f.read())
    version = old_version


def usage():
    print(
        f"Usage: {sys.executable} {sys.argv[0]} [ major | minor | patch | prerelease | build ]"
    )
    sys.exit(0)


def run_command(command: str):
    if os.system(command):
        print(f'\n\nCommand "{command}" failed.')
        os.system("git reset --hard")
        sys.exit(1)


prerelease = False

if len(sys.argv) == 1:
    usage()
    sys.exit(1)

match sys.argv[1].lower():
    case "major":
        version = version.bump_major()
    case "minor":
        version = version.bump_minor()
    case "patch":
        version = version.bump_patch()
    case "prerelease":
        version = version.bump_prerelease()
        prerelease = True
    case "build":
        version = version.bump_build()
    case arg:
        print(f"Unknown argument `{arg}`")
        usage()
        sys.exit(1)


print(f"{old_version} -> {version}")
choice = input("Create release? [N/y] ").lower()

if choice != "y":
    sys.exit(0)

run_command("task lint && task format")


with open("version", "w") as f:
    f.write(str(version))

with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f).unwrap()
pyproject["project"]["version"] = str(version)

with open("pyproject.toml", "w") as f:
    toml.dump(pyproject, f)

with open("CHANGELOG.md", "r") as f:
    changes = changelog.loads(f.read())

for change in changes:
    if str(change["version"]).lower() == "unreleased":
        change["version"] = version
        change["date"] = date.today()
        changes.insert(
            0,
            {
                "version": "Unreleased",
            },
        )
        break


with open("CHANGELOG.md", "w") as f:
    f.write(changelog.dumps(changes))


with open("CHANGELOG.md") as f:
    changes = changelog.load(f)[1]


content = changelog.dumps([changes], "").strip()

if match := re.match(r"## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}", content):
    content = content.replace(match.group(0), "").strip()

with open("release_body.md", "w") as f:
    f.write(content)



run_command("poetry build")
run_command("poetry publish")
run_command('git add . && git commit -a -m "bump version" && git push')

run_command(
    f'gh release create v{version} --target main --notes-file release_body.md {"-p" if prerelease else ""} --title v{version}'
)
run_command("rm release_body.md")

print("\n\nRelease successfully created and published.\n\n")
run_command("git fetch --tags")
