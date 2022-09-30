from random import randint
from .SongData import SongData


def interpolate(x, x0, y0, x1, y1):
    return y1 + (x - x0) * ((y1 - y0) / (x1 - x0))


class UbiArtMap:
    """UbiArt map"""

    def __init__(self, beats: list, song_data: SongData):
        """Constructor"""
        self.beats = self._convert_beats(beats)
        
        self.song_data = song_data
        self.clips = []

    def _convert_beats(self, beats: list):
        """Convert beats to UbiArt format"""
        return list(map(lambda x: x * 48000, beats)) # input data have to be seconds
                                                     # milliseconds * 48 = (seconds * 1000) * 48 = seconds * 48000

    def _interpolate_time(self, time: float) -> int:
        return int(interpolate(time, self.beats[0] / 48000, self.beats[-1] / 48000, self.beats[0], self.beats[-1]))

    def add_pictogram_clip(self, pictogram_data: dict):
        """Add pictogram clip"""
        pictogram_clip = {
            "__class": "PictogramClip",
            "Id": randint(0, 4294967294),
            "TrackId": randint(0, 4294967294),
            "IsActive": 1,
            "StartTime": self._interpolate_time(pictogram_data["time"]),
            "Duration": 24,
            "PictoPath": f"world/maps/{self.song_data.userfriendly_id.lower()}/timeline/pictos/{pictogram_data['texture_path'].split('/')[-1]}.png",
            "AtlIndex": 4294967295,
            "CoachIndex": 4294967295
        }
        
        self.clips.append(pictogram_clip)
        self._resort_clips()

    def _resort_clips(self) -> None:
        """Resort clips by ID and TrackID"""
        self.clips.sort(lambda x: x["Id"] + x["TrackId"])

    def generate_dance_tape(self) -> dict:
        """Generate dance tape"""

        return {
            "__class": "Tape",
            "Clips": self.clips,
            "TapeClock": 0,
            "TapeBarCount": 1,
            "FreeResourcesAfterPlay": 0,
            "MapName": self.song_data.userfriendly_id,
            "SoundwichEvent": ""
        }

    def generate_musictrack(self) -> dict:
        """Generate musictrack"""

        return {}

    def generate_song_description(self) -> dict:
        """Generate song description asset"""

        return {}


__all__ = ["UbiArtMap"]
