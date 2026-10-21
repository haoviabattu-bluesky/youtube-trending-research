# -*- coding: utf-8 -*-
"""Đường dự phòng cuối khi MỌI đường phụ đề bị chặn (2026-10-11: api + yt-dlp IpBlocked, timedtext 429 cả trong Chrome thật,
proxy VÂN bị từ chối). Luồng tải video/audio (googlevideo) KHÔNG bị chặn → tải audio, cắt N giây đầu, nhận dạng giọng
bằng faster-whisper. Chữ là ASR của mình nên gắn nhãn [asr, chưa kiểm] khi trích.

    py -3.13 -X utf8 src/transcript_asr.py VIDEO_ID [--sec 120]
"""
import glob, os, subprocess, sys, tempfile

FFMPEG = r"E:\CLAUDE\MOTION GRAPHICS\tools\ffmpeg\bin\ffmpeg.exe"
_MODEL = None


def _model():
    global _MODEL
    if _MODEL is None:
        from faster_whisper import WhisperModel
        _MODEL = WhisperModel(os.environ.get("ASR_MODEL", "small"), device="cpu", compute_type="int8")
    return _MODEL


def fetch(vid, lang="ja", sec=120):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "--js-runtimes", "node", "-f", "ba[ext=m4a]/ba/b",  # 15/10: thiếu JS runtime → "format not available"
                        "-o", os.path.join(tmp, "a.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"],
                       check=True, capture_output=True, timeout=600)
        src = glob.glob(os.path.join(tmp, "a.*"))[0]
        wav = os.path.join(tmp, "cut.wav")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-t", str(sec), "-ac", "1", "-ar", "16000", wav],
                       check=True, timeout=300)
        segs, _ = _model().transcribe(wav, language=lang, vad_filter=True)
        return [{"start": round(s.start, 2), "duration": round(s.end - s.start, 2), "text": s.text.strip()} for s in segs]


if __name__ == "__main__":
    sec = int(sys.argv[sys.argv.index("--sec") + 1]) if "--sec" in sys.argv else 120
    for x in fetch(sys.argv[1], sec=sec):
        print(f'[{int(x["start"])//60}:{int(x["start"])%60:02d}] {x["text"]}')
