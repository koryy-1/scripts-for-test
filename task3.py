import json
import re


def generate_versions(version, config_file):
    with open(config_file, "r") as f:
        templates: dict = json.load(f)

    generated = []

    for key, template in templates.items():
        parts = template.split(".")
        stars = parts.count("*")
        if stars == 0:
            generated.append(template)
            continue

        for i in range(2):
            gen = []
            for part in parts:
                if part == "*":
                    gen.append(str((i + 1) * 3))
                else:
                    gen.append(part)
            generated.append(".".join(gen))

    sorted_versions = sorted(generated, key=lambda s: list(map(int, s.split("."))))
    print("Все сгенерированные версии:")
    for v in sorted_versions:
        print(v)

    input_version = list(map(int, version.split(".")))
    older = [v for v in sorted_versions if list(map(int, v.split("."))) < input_version]
    print("\nВерсии меньше переданной:")
    for v in older:
        print(v)


# Пример запуска:
# generate_versions('3.7.4', 'config.json')
