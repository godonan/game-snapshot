from PIL import Image
import mss


class TakeSnapshot:
    @classmethod
    def take_screenshot(cls, monitor_id=1):
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[monitor_id]
            screenshot = mss_instance.grab(monitor)
            image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return image
