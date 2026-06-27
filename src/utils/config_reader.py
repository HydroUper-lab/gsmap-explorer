
def read_config(path):
    config = {}

    with open(path) as f:
        for line in f:
            line = line.strip()

            # skip kosong & komentar penuh
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, val = line.split("=", 1)

            # ✅ buang komentar di belakang nilai
            val = val.split("#", 1)[0].strip()

            config[key.strip()] = val

    return config


# if __name__ == "__main__":
#     config = read_config("config/input.txt")
#     print(config)
