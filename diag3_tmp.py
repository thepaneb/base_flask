"""Inspeciona o runs do action (apagar após uso)."""

import urllib.request

url = "https://raw.githubusercontent.com/googleapis/release-please-action/v4/action.yml"
data = urllib.request.urlopen(url, timeout=30).read().decode()
i = data.find("runs:")
print(data[i : i + 800])
