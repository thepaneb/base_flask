"""Inspeciona o action.yml do release-please v4 (apagar após uso)."""

import urllib.request

for ref in ["v4", "v4.0.0", "main"]:
    try:
        url = f"https://raw.githubusercontent.com/googleapis/release-please-action/{ref}/action.yml"
        data = urllib.request.urlopen(url, timeout=30).read().decode()
        print("=" * 20, ref, "=" * 20)
        print(data[:3000])
        break
    except Exception as e:
        print(ref, "->", e)
