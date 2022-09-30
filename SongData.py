import Constants

class SongData:
    """Song data"""

    def __init__(self, raw_data: dict) -> None:'
        """Constructor"""
        self.id = raw_data["id"]
        self.material_number = raw_data["materialNo"]
        self.title = raw_data["materialName"]
        self.artist = raw_data["singer"]
        self.userfriendly_id = raw_data["info"]
        self.mv_urls = {
            "super": raw_data["fullMvDTO"]["fullMvSuper"],
            "high": raw_data["fullMvDTO"]["fullMvHigh"],
            "middle": raw_data["fullMvDTO"]["fullMvMiddle"],
            "clear": raw_data["fullMvDTO"]["fullMvClears"]
        }
        self.play_model = raw_data["playModel"]
        self.dancer_count = 1 if raw_data["playNumberPeople"] == "single_people" else 2
        self.duration = raw_data["mvPeriod"]

    def generate_beats(self) -> list:
        """Beat generator"""
        result = [0]
        beat_size = (Constants.DEFAULT_BPM / 60000) / 1000 # seconds is based

        while result[-1] > self.duration:
            current_beat = result[-1] + beat_size
            result.append(current_beat)

        return result

__all__ = ["SongData"]
