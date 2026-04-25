"""
GIF Recorder for TinyProgrammer canvas.

Call start() at the top of the WATCH loop, capture(surface) inside
each tick, and stop() when done.
"""

import io
import time
from typing import Optional, List


class GifRecorder:

    def __init__(self):
        self._frames: List = []
        self._fps: int = 10
        self._max_duration: int = 30
        self._last_capture: float = 0.0
        self._start_time: float = 0.0
        self._active: bool = False

    @property
    def is_active(self) -> bool:
        return self._active

    def start(self, fps: int = 10, max_duration: int = 30) -> None:
        self._frames = []
        self._fps = max(1, min(30, fps))
        self._max_duration = max(1, max_duration)
        self._last_capture = 0.0
        self._start_time = time.monotonic()
        self._active = True
        print(f"[GifRecorder] Started ({self._fps} fps, max {self._max_duration}s)")

    def capture(self, surface) -> None:

        if not self._active:
            return

        now = time.monotonic()
        if now - self._start_time >= self._max_duration:
            self._active = False
            return

        if now - self._last_capture < 1.0 / self._fps:
            return

        try:
            import pygame
            from PIL import Image

            arr = pygame.surfarray.array3d(surface)
            arr = arr.transpose(1, 0, 2)
            img = Image.fromarray(arr.astype("uint8"), "RGB")
            img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            self._frames.append(img)
            self._last_capture = now
        except Exception as e:
            print(f"[GifRecorder] Capture error: {e}")

    def stop(self) -> Optional[bytes]:
        self._active = False
        result = self._encode()
        frame_count = len(self._frames)
        self._frames = []
        if result:
            print(f"[GifRecorder] Encoded {frame_count} frames → {len(result):,} bytes")
        else:
            print("[GifRecorder] No frames captured — GIF skipped")
        return result

    def _encode(self) -> Optional[bytes]:
        if not self._frames:
            return None

        frame_ms = max(20, int(1000 / self._fps))
        try:
            buf = io.BytesIO()
            self._frames[0].save(
                buf,
                format="GIF",
                save_all=True,
                append_images=self._frames[1:],
                loop=0,
                duration=frame_ms,
                optimize=False,
            )
            return buf.getvalue()
        except Exception as e:
            print(f"[GifRecorder] Encode error: {e}")
            return None
