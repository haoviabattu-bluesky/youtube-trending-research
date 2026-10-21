# -*- coding: utf-8 -*-
"""TÌM + ĐỌC trang tư liệu, trích số liệu [Dn] bằng model ngoài (gate ext_extract) — thay subagent Opus.

Luật giữ nguyên: "số nào cũng phải có trang mở được". Model phải chép CÂU NGUYÊN VĂN chứa số; Python kiểm
câu đó là chuỗi con của trang đã tải (chuẩn hoá NFKC, bỏ khoảng trắng) và con số có nằm trong câu.
Không khớp → loại, ghi vào `bi_loai` (không bao giờ vào tu_lieu). Bản chữ trang lưu ở <out>/nguon/ để kiểm lại.

    py -3.13 -X utf8 src/source_extract.py --q "tỉ lệ 50代 bị giảm lương sau 再雇用" \
        --search "再雇用 賃金 減少 割合 調査" --search "定年後 再雇用 年収 下がる 統計" \
        [--urls https://... ...] [--grep 再雇用,賃金] --out data/x/tu_lieu [--per-query 4]
Tìm web dùng Chrome nền chung (pw_search.py, cổng 9461) — không mở/tắt cửa sổ.
"""
from __future__ import annotations

import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\MG_STUDIO")
from ext_llm import ask_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PW = ROOT / "data" / "lane_q_topics_20261010" / "pw_search.py"
GATE, MAXCH = "ext_extract", 14000
SKIP = re.compile(r"youtube\.com|youtu\.be|x\.com|twitter\.com|facebook\.com|instagram\.com|tiktok\.com")
PROMPT = """Câu hỏi tư liệu: {q}
Đọc văn bản trang dưới đây (nguồn: {url}). Trích MỌI số liệu / sự kiện trả lời được câu hỏi.
LUẬT: "nguyen_van" phải là đoạn CHÉP Y NGUYÊN từ văn bản (tiếng gốc, 15–160 ký tự, chứa con số) — không dịch,
không sửa, không gộp hai câu. Không có thì trả list rỗng. Giải thích bằng tiếng Việt.
Trả DUY NHẤT JSON: {{"facts":[{{"so_lieu":"con số đúng như trong câu, vd 44.2%","nguyen_van":"...",
"y_nghia_vi":"câu tiếng Việt: số này nói gì","thoi_diem":"năm/tháng khảo sát nếu có","don_vi_cong_bo":"tổ chức công bố nếu có"}}]}}
VĂN BẢN:
{text}"""


def chuan(s: str) -> str:
    from core.web_text import chuan as c
    return c(s)


def verify(fact: dict, page_text: str) -> str | None:
    """None = đạt. Ngược lại trả lý do loại."""
    q, n = fact.get("nguyen_van") or "", fact.get("so_lieu") or ""
    if len(chuan(q)) < 8:
        return "câu trích quá ngắn"
    if chuan(q) not in chuan(page_text):
        return "câu trích KHÔNG có trong trang"
    digits = re.findall(r"\d+(?:[.,]\d+)?", chuan(n))
    if not digits:
        return "không có con số"
    if not all(d in chuan(q) for d in digits):
        return "con số không nằm trong câu trích"
    return None


def search_urls(query: str, k: int) -> list[str]:
    out = subprocess.run([sys.executable, "-X", "utf8", str(PW), "g", query], capture_output=True, text=True,
                         encoding="utf-8", errors="ignore", timeout=180).stdout
    urls = [m.group(1) for m in re.finditer(r"^- .*? \| (https?://\S+) \|", out, re.M)]
    return [u for u in dict.fromkeys(urls) if not SKIP.search(u)][:k]


def _chrome_page(url: str) -> tuple[str, str, str]:
    """Mở TAB RIÊNG trên Chrome nền chung (cổng 9461) rồi đóng tab đó — không đụng cửa sổ/tab khác.
    Trả URL CUỐI (link google.com/goto của kết quả Google chỉ chuyển hướng bằng JS, requests không giải được)."""
    import time
    from core import web_text as W
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, str(PW.parent))
    import pw_search as P
    with sync_playwright() as p:
        ctx = p.chromium.connect_over_cdp(P.ensure_chrome()).contexts[0]
        pg = ctx.new_page()
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2.5)
            final = pg.url
            if final.lower().split("?")[0].endswith(".pdf"):
                t, x = W._pdf(ctx.request.get(final).body())
            else:
                t, x = W._html(pg.content().encode("utf-8"), "utf-8")
            return t, x, final
        finally:
            pg.close()


def load_page(url: str) -> tuple[str, str, str]:
    """(tiêu đề, chữ trang, URL cuối). requests trước (nhanh), hỏng/ít chữ/link chuyển hướng → Chrome nền."""
    from core.web_text import tai
    if "google.com/goto" not in url and "google.com/url" not in url:
        try:
            title, text = tai(url)
            if len(text) >= 300:
                return title, text, url
        except Exception:
            pass
    try:
        return _chrome_page(url)
    except Exception:
        return "", "", url


def focus(text: str, grep: list[str]) -> str:
    """Trang dài: giữ cửa sổ quanh từ khoá thay vì cắt đầu trang (số hay nằm giữa báo cáo)."""
    if len(text) <= MAXCH or not grep:
        return text[:MAXCH]
    spans = sorted({max(0, m.start() - 600) for k in grep for m in re.finditer(re.escape(k), text)})
    parts, last = [], -1
    for a in spans:
        if a > last:
            parts.append(text[a:a + 1400]); last = a + 1400
        if sum(map(len, parts)) > MAXCH:
            break
    return "\n…\n".join(parts) or text[:MAXCH]


def run(q: str, urls: list[str], grep: list[str], out: Path, start_d: int) -> dict:
    (out / "nguon").mkdir(parents=True, exist_ok=True)
    db_p = out / "tu_lieu.json"
    db = json.loads(db_p.read_text(encoding="utf-8")) if db_p.exists() else {"tu_lieu": [], "bi_loai": [], "trang": []}
    have = {(f["url"], chuan(f["nguyen_van"])) for f in db["tu_lieu"]}
    nxt = max([int(f["id"][1:]) for f in db["tu_lieu"]] + [start_d - 1]) + 1
    log = []
    for url in urls:
        title, text, url = load_page(url)
        if SKIP.search(url):
            log.append(f"· bỏ {url} (mạng xã hội/video)"); continue
        if len(text) < 300:
            log.append(f"✗ {url} — không đọc được trang"); db["trang"].append({"url": url, "ok": False}); continue
        h = hashlib.md5(url.encode()).hexdigest()[:10]
        (out / "nguon" / f"{h}.txt").write_text(f"{title}\n{url}\n\n{text}", encoding="utf-8")
        res = ask_json(GATE, PROMPT.format(q=q, url=url, text=focus(text, grep)), ids=[h])
        facts = (res.parsed_response or {}).get("facts", []) if res.ok and isinstance(res.parsed_response, dict) else []
        kept = 0
        for f in facts if isinstance(facts, list) else []:
            if not isinstance(f, dict):
                continue
            why = verify(f, text)
            base = {**f, "url": url, "trang": title[:100], "file_nguon": f"nguon/{h}.txt", "model": res.model}
            if why:
                db["bi_loai"].append({**base, "ly_do": why}); continue
            if (url, chuan(f["nguyen_van"])) in have:
                continue
            have.add((url, chuan(f["nguyen_van"])))
            db["tu_lieu"].append({"id": f"D{nxt}", **base}); nxt += 1; kept += 1
        db["trang"].append({"url": url, "ok": True, "title": title[:100], "giu": kept, "model": res.model,
                            "loi": res.error})
        log.append(f"{'✓' if kept else '·'} {kept} số · {title[:50]} · {url}" + (f" ⚠ {res.error}" if res.error else ""))
    db_p.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"log": log, "db": db, "path": db_p}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--search", action="append", default=[])
    ap.add_argument("--urls", nargs="*", default=[])
    ap.add_argument("--grep", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-query", type=int, default=4)
    ap.add_argument("--start-d", type=int, default=1)
    a = ap.parse_args()
    urls = list(a.urls)
    for s in a.search:
        urls += search_urls(s, a.per_query)
    urls = list(dict.fromkeys(urls))
    r = run(a.q, urls, [k for k in a.grep.split(",") if k], Path(a.out), a.start_d)
    print("\n".join(r["log"]))
    for f in r["db"]["tu_lieu"][-15:]:
        print(f'[{f["id"]}] {f["so_lieu"]} — {f["y_nghia_vi"][:90]} ({f.get("don_vi_cong_bo", "")} {f.get("thoi_diem", "")})')
    print(f'→ {r["path"]} · giữ {len(r["db"]["tu_lieu"])} · loại {len(r["db"]["bi_loai"])} (câu trích không khớp trang)')


if __name__ == "__main__":
    main()
