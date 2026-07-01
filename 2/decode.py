import yaml
import redis

title = ""
author = ""
inspiration = []
stanzas = {}

redis = redis.Redis(host="localhost", port=6379)
passkey = b"ggw3llpl4y3d!"

def decode(redis_key):
	encoded = redis.get(redis_key)
	decoded = bytearray()
	for i in range(len(encoded)):
		decoded.append(encoded[i] ^ passkey[i % len(passkey)])
	return decoded.decode("utf-8", errors="replace")

keys = [key.decode() for key in redis.keys("*")]

for key in keys:
    match key:
        case "title":
            title = decode(key)
        case "author":
            author = decode(key)
        case "thekeyisthere":
            continue
        case k if k.startswith("inspiration."):
            inspiration.append((key, decode(key)))
        case k if k.startswith("verses."):
            parts = key.split(".")
            stanza_num = int(parts[1].replace("stanza", ""))
            line_num = int(parts[2].replace("line", ""))
            stanzas.setdefault(stanza_num, {})[line_num] = decode(key)

inspiration.sort(key=lambda pair: int(pair[0].split("line")[1]))
inspiration = [text for key, text in inspiration]

ordered_stanzas = []
for stanza_num in sorted(stanzas):
    lines = stanzas[stanza_num]
    ordered_lines = [lines[i] for i in sorted(lines)]
    ordered_stanzas.append({"lines": ordered_lines})

poem = {
    "title": title,
    "author": author,
    "inspiration": inspiration,
    "stanzas": ordered_stanzas,
}

class IndentedDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

with open("poem.yaml", "w", encoding="utf-8") as f:
    yaml.dump(poem, f, allow_unicode=True, sort_keys=False, Dumper=IndentedDumper, indent=2)