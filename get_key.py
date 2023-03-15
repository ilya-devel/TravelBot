def get_key():
    with open('.tgmBot.key', 'r') as f:
        key = f.read()
    return key.strip()
