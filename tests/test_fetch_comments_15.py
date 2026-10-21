# -*- coding: utf-8 -*-
"""Test chính thức cho `fetch_comments_15.py` — Lane J (`teinengo-fuufu`).

VÌ SAO CÓ FILE NÀY: script gom bình luận chỉ có verify ad-hoc trong phiên
⇒ bộ theo dõi thay đổi của workspace không gắn được chứng cứ ⇒ file luôn bị
đánh dấu "unverified" dù đã chạy đúng. File test này là chỗ gắn chứng cứ.

ĐẶT TRONG `tests/` (không phải cạnh file nguồn) vì dự án ĐÃ CÓ hạ tầng test ở
đây: `tests/conftest.py` + 5 file test chạy tốt (52 passed). Đặt cạnh file nguồn
trong `scratch_golo/` thì không nằm trong đường chạy test canonical của dự án.
`tests/conftest.py` chỉ thêm `src/` vào sys.path (KHÔNG thêm `scratch_golo/`)
⇒ file này tự nạp module nguồn bằng đường dẫn tuyệt đối.

Chạy (từ gốc dự án):
    env -u PYTHONPATH py -3.13 -m pytest tests/ -q
    env -u PYTHONPATH py -3.13 -m pytest tests/test_fetch_comments_15.py -q

⚠️ `env -u PYTHONPATH` là BẮT BUỘC — PYTHONPATH của Hermes trỏ venv cp311 làm
`py -3.13` vỡ numpy/PIL. `dotenv` phải có trong môi trường py -3.13.

⚠️ Test KHÔNG gọi mạng. `urllib.request.urlopen` được thay bằng hàm giả để
(1) bắt URL thật gửi lên YouTube, (2) ép phân trang, (3) giả lập commentsDisabled.
"""
from __future__ import annotations

import importlib.util
import io
import json
import urllib.parse
from pathlib import Path

import pytest

SC = Path(__file__).resolve().parent.parent / "scratch_golo"
TARGET = SC / "fetch_comments_15.py"


# ────────────────────────────────────────────────────────────── nạp module
@pytest.fixture(scope="module")
def fc():
    """Nạp `fetch_comments_15.py` mà KHÔNG chạy `main()`."""
    spec = importlib.util.spec_from_file_location("fetch_comments_15", TARGET)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # guard __main__ chặn main()
    return mod


@pytest.fixture(autouse=True)
def _khong_ngu_thuc(fc, monkeypatch):
    """⛔ KHÔNG ngủ thật trong test.

    Đã dính: để `time.sleep` nguyên ⇒ 2 test chậm nhất 35s + 15s vì `api()`
    retry backoff (1,5+3,0+4,5+6,0 = 15s) và vòng phân trang. Test phải
    NHANH — sleep thật là dấu hiệu test đang chạm mạng/backoff thật.
    """
    monkeypatch.setattr(fc.time, "sleep", lambda *_: None)


class FakeResp(io.StringIO):
    """Giả `urlopen` context manager."""

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


@pytest.fixture
def mock_net(fc, monkeypatch):
    """Thay urlopen; trả (calls, set_item, set_raise) để điều khiển phản hồi."""
    calls: list[str] = []
    state = {"item": lambda page: {"textDisplay": "x", "likeCount": 1,
                                   "authorDisplayName": "a"},
             "next": None,          # nextPageToken trả về (xem `next_once`)
             "raise": None}         # exception cần ném

    def fake_urlopen(url, timeout=None):
        calls.append(url)
        if state["raise"] is not None:
            raise state["raise"]
        page = urllib.parse.parse_qs(
            urllib.parse.urlparse(url).query).get("pageToken", [None])[0]
        s = state["item"](page)
        out = {"items": [{"snippet": {"topLevelComment": {"snippet": s}}}]}
        # `next` là token trả MỘT LẦN rồi hết — tránh vòng lặp vô hạn
        # (đã dính: `next="TOK2"` mãi ⇒ ~100 lần gọi, test 35s).
        if state["next"] and page is None:
            out["nextPageToken"] = state["next"]
        return FakeResp(json.dumps(out))

    monkeypatch.setattr(fc.urllib.request, "urlopen", fake_urlopen)
    return calls, state


# ─────────────────────────────────────────────────── 1. cấu trúc / nạp module
def test_target_ton_tai():
    assert TARGET.exists(), f"thiếu {TARGET}"
    assert TARGET.stat().st_size > 2000


def test_compile_sach():
    compile(TARGET.read_text(encoding="utf-8"), str(TARGET), "exec")


def test_nap_khong_chay_main(fc):
    """Nạp module KHÔNG được gọi API (guard `__main__` phải có)."""
    src = TARGET.read_text(encoding="utf-8")
    assert 'if __name__ == "__main__":' in src
    assert not hasattr(fc, "_da_chay_main"), "module nạp đã chạy main()"


def test_hang_so(fc):
    assert fc.MAX == 100, "trần API commentThreads là 100"
    assert 0 < fc.SLEEP <= 2, "SLEEP phải hợp lý để tránh rate limit"


@pytest.mark.parametrize("fn", ["api", "comments_of", "main"])
def test_co_ham(fc, fn):
    assert callable(getattr(fc, fn, None)), f"thiếu hàm {fn}()"


# ──────────────────────────────────────────── 2. api(): endpoint + tham số
def test_api_dung_endpoint(fc, mock_net):
    calls, _ = mock_net
    d = fc.api("commentThreads", videoId="ABC", maxResults=100)
    assert isinstance(d, dict)
    assert calls, "chưa gọi urlopen"
    assert "googleapis.com/youtube/v3/commentThreads" in calls[0], calls[0]


def test_api_gui_key_va_videoid(fc, mock_net):
    calls, _ = mock_net
    fc.api("commentThreads", videoId="ABC")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(calls[0]).query)
    assert "key" in q, "thiếu API key"
    assert q["videoId"] == ["ABC"]


# ──────────────────── 3. comments_of(): tham số + phân trang + trần MAX
def test_params_gui_len_youtube(fc, mock_net, monkeypatch):
    """Đúng 4 tham số quyết định chất lượng dữ liệu."""
    monkeypatch.setitem(fc.__dict__, "MAX", 100)
    calls, _ = mock_net
    fc.comments_of("ABC")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(calls[0]).query)
    assert q.get("part") == ["snippet"]
    assert q.get("order") == ["relevance"], "phải xếp theo độ liên quan"
    assert q.get("textFormat") == ["plainText"], "plainText để tránh rác HTML"
    assert q.get("maxResults") == ["100"]


def test_phan_trang_chay_that(fc, mock_net):
    """Ép nextPageToken ⇒ phải gọi trang 2 kèm pageToken."""
    calls, state = mock_net
    state["next"] = "TOK2"
    fc.comments_of("ABC")
    assert len(calls) >= 2, f"phân trang không chạy (chỉ {len(calls)} lần gọi)"
    q2 = urllib.parse.parse_qs(urllib.parse.urlparse(calls[1]).query)
    assert q2.get("pageToken") == ["TOK2"], q2


def test_ton_trong_tran_max(fc, monkeypatch):
    """Không bao giờ trả quá MAX dù API còn trang.

    ⚠️ Bẫy đã dính: bản đầu cho mỗi trang trả **1** item ⇒ vòng
    `while len(out) < MAX` tự dừng đúng MAX, nên `out[:MAX]` thành **dư thừa**
    ⇒ mutation test bỏ `out[:MAX]` mà test vẫn pass (test pass giả).
    Phải cho mỗi trang trả NHIỀU item để `out` vượt MAX trong 1 lần lặp —
    lúc đó `out[:MAX]` mới thật sự có tác dụng và mới kiểm được.
    """
    monkeypatch.setitem(fc.__dict__, "MAX", 3)

    calls: list[str] = []

    def fake(url, timeout=None):
        calls.append(url)
        # 1 trang trả 10 item: 0 -> 10, vượt MAX=3 ngay lần lặp đầu
        items = [{"snippet": {"topLevelComment": {"snippet": {
            "textDisplay": f"c{i}", "likeCount": 1, "authorDisplayName": "a"}}}}
            for i in range(10)]
        return FakeResp(json.dumps({"items": items, "nextPageToken": "TOK"}))

    monkeypatch.setattr(fc.urllib.request, "urlopen", fake)
    got = fc.comments_of("ABC")
    assert len(got) == 3, f"trả {len(got)} — phải cắt đúng MAX=3"
    assert len(calls) == 1, f"gọi {len(calls)} lần — phải dừng sau 1 trang"


def test_schema_binh_luan(fc, mock_net):
    calls, _ = mock_net
    got = fc.comments_of("ABC")
    assert got and set(got[0]) == {"text", "votes", "author"}, set(got[0])


def test_votes_la_chuoi(fc, mock_net):
    """API trả likeCount dạng số nhưng script lưu str — giữ nguyên để so sánh thống nhất."""
    calls, _ = mock_net
    got = fc.comments_of("ABC")
    assert isinstance(got[0]["votes"], str), type(got[0]["votes"]).__name__


def test_votes_giu_dung_GIA_TRI_likecount(fc, mock_net):
    """`votes` phải là CHÍNH likeCount, không phải hằng số.

    ⚠️ Bẫy đã dính: chỉ kiểm `isinstance(votes, str)` thì việc đổi thành
    `"0"` cứng vẫn pass (mutation test bắt được lỗ hổng này). Phải kiểm GIÁ TRỊ,
    và kiểm 2 giá trị KHÁC NHAU để chắc không phải hằng số.
    """
    calls, state = mock_net
    for like in (7, 469):
        state["item"] = lambda page, _l=like: {
            "textDisplay": "x", "likeCount": _l, "authorDisplayName": "a"}
        got = fc.comments_of("ABC")
        assert got[0]["votes"] == str(like), \
            f"likeCount={like} nhưng votes={got[0]['votes']!r}"


def test_votes_mac_dinh_0_khi_api_thieu_truong(fc, mock_net):
    """API có thể bỏ hẳn `likeCount` ⇒ phải mặc định '0', không crash."""
    calls, state = mock_net
    state["item"] = lambda page: {"textDisplay": "x", "authorDisplayName": "a"}
    got = fc.comments_of("ABC")
    assert got[0]["votes"] == "0", got[0]["votes"]


def test_author_giu_dung_gia_tri(fc, mock_net):
    calls, state = mock_net
    state["item"] = lambda page: {"textDisplay": "x", "likeCount": 1,
                                  "authorDisplayName": "鈴木太郎"}
    assert fc.comments_of("ABC")[0]["author"] == "鈴木太郎"


def test_text_duoc_strip(fc, mock_net):
    calls, state = mock_net
    state["item"] = lambda page: {"textDisplay": "  xin chao  ",
                                  "likeCount": 0, "authorDisplayName": "a"}
    got = fc.comments_of("ABC")
    assert got[0]["text"] == "xin chao"


# ────────────────── 4. lỗi API: commentsDisabled ⇒ không retry vô ích
class _Err(Exception):
    """Giả 403 có `read()` như HTTPError."""

    def __init__(self, reason: str):
        self.reason = reason

    def read(self):
        return json.dumps(
            {"error": {"errors": [{"reason": self.reason}]}}).encode()


@pytest.mark.parametrize("reason", ["commentsDisabled", "videoNotFound"])
def test_khong_retry_khi_loi_vinh_vien(fc, mock_net, reason):
    calls, state = mock_net
    state["raise"] = _Err(reason)
    got = fc.comments_of("XYZ")
    assert got == [], f"phải trả [] (nhận {got})"
    assert len(calls) == 1, f"retry vô ích {len(calls)} lần"


def test_khong_crash_khi_json_json_loi(fc, mock_net):
    """Lỗi mạng thường (không có `read`) vẫn phải bị bắt, không ném ra ngoài."""
    calls, state = mock_net
    state["raise"] = TimeoutError("mạng chậm")
    assert fc.comments_of("ABC") == []


# ──────────────────────────── 5. artifact THẬT do script sinh ra (nếu đã chạy)
ARTIFACT = SC / "comments_15videos.json"
DOI_VIDEO = 15


@pytest.fixture(scope="module")
def data():
    if not ARTIFACT.exists():
        pytest.skip(f"chưa có {ARTIFACT.name} — chạy fetch_comments_15.py trước")
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_artifact_ton_tai():
    assert ARTIFACT.exists(), f"thiếu {ARTIFACT}"
    assert ARTIFACT.stat().st_size > 1000


def test_phu_du_so_video(data):
    assert len(data) == DOI_VIDEO, f"phủ {len(data)}/{DOI_VIDEO}"


def test_moi_video_co_binh_luan(data):
    thieu = [v for v, o in data.items() if not o.get("comments")]
    assert not thieu, f"video không có bình luận: {thieu}"


def test_schema_tung_binh_luan(data):
    for vid, o in data.items():
        for c in o["comments"]:
            assert set(c) == {"text", "votes", "author"}, (vid, set(c))


def test_khong_co_text_rong(data):
    rong = [(v, c) for v, o in data.items() for c in o["comments"] if not c["text"].strip()]
    assert not rong, f"{len(rong)} bình luận rỗng"


def test_khong_vuot_tran_100_moi_video(data):
    mx = max(len(o["comments"]) for o in data.values())
    assert mx <= 100, f"có video {mx} bình luận > trần 100"


def test_giu_metadata_tu_handoff(data):
    thieu = [v for v, o in data.items() if "uu_tien" not in o]
    assert not thieu, f"thiếu trường uu_tien: {thieu}"


def test_ban_doc_nguoi_ton_tai(data):
    md = SC / "comments_15videos.md"
    assert md.exists(), f"thiếu {md}"
    assert md.stat().st_size > 1000
    # mỗi video ưu tiên phải có mục trong bản đọc người
    t = md.read_text(encoding="utf-8")
    for vid in data:
        assert vid in t, f"{vid} không có trong bản .md"
