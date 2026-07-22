import urllib.request

version = "3.22.3"
urls = [
    ("Flutter official (geo-blocked)", f"https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_{version}-stable.zip"),
    ("Huawei Cloud mirror", f"https://mirrors.huaweicloud.com/flutter/flutter_infra_release/releases/stable/windows/flutter_windows_{version}-stable.zip"),
    ("Tencent Cloud mirror", f"https://mirrors.tencent.com/flutter/flutter_infra_release/releases/stable/windows/flutter_windows_{version}-stable.zip"),
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0")
        resp = urllib.request.urlopen(req, timeout=15)
        size = resp.headers.get("Content-Length", "?")
        print(f"[OK] {name}: {resp.status} ({size} bytes)")
    except urllib.error.HTTPError as e:
        print(f"[{e.code}] {name}: {e.reason}")
    except Exception as e:
        print(f"[ERR] {name}: {type(e).__name__}")
