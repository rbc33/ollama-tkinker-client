import subprocess


def list_models():
    output = subprocess.Popen(["ollama", "list"], stdout=subprocess.PIPE).communicate()[
        0
    ]
    # print(output.decode("utf-8"))
    mod_draft = []
    for line in output.decode("utf-8").split("\n"):
        if line:
            mod = line.split()[0]
            mod_draft.append(mod)

    models = mod_draft[1:]
    clean_names = []
    for model in models:
        if model.endswith(":latest"):
            clean_names.append(model[:-7])
        else:
            clean_names.append(model)

    return clean_names


if __name__ == "__main__":
    models = list_models()
    for model in models:
        print(model)
