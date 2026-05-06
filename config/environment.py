def get_config():
    config = {}
    with open("config/config.yaml") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            config[key.strip().strip('"')] = value.strip().strip('"')
    return config