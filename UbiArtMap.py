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

        return {
            "__class": "Actor_Template",
            "WIP": 0,
            "LOWUPDATE": 0,
            "UPDATE_LAYER": 0,
            "PROCEDURAL": 0,
            "STARTPAUSED": 0,
            "FORCEISENVIRONMENT": 0,
            "COMPONENTS": [{
                    "__class": "MusicTrackComponent_Template",
                    "trackData": {
                        "__class": "MusicTrackData",
                        "structure": {
                            "__class": "MusicTrackStructure",
                            "markers": self.beats,
                            "signatures": [{
                                    "__class": "MusicSignature",
                                    "marker": 0,
                                    "beats": 4
                                }
                            ],
                            "startBeat": 0,
                            "endBeat": len(self.beats),
                            "fadeStartBeat": 0,
                            "useFadeStartBeat": false,
                            "fadeEndBeat": 0,
                            "useFadeEndBeat": false,
                            "videoStartTime": 0,
                            "previewEntry": len(self.beats) / 6,
                            "previewLoopStart": len(self.beats) / 6,
                            "previewLoopEnd": len(self.beats) / 4,
                            "volume": 0,
                            "fadeInDuration": 0,
                            "fadeInType": 0,
                            "fadeOutDuration": 0,
                            "fadeOutType": 0
                        },
                        "path": f"world/maps/{self.song_data.userfriendly_id.lower()}/audio/{self.song_data.userfriendly_id.lower()}.wav",
                        "url": f"jmcs://jd-contents/{self.song_data.userfriendly_id}/{self.song_data.userfriendly_id}.ogg"
                    }
                }
            ]
        }

    def generate_song_description(self) -> dict:
        """Generate song description asset"""

        return {
            "__class": "Actor_Template",
            "WIP": 0,
            "LOWUPDATE": 0,
            "UPDATE_LAYER": 0,
            "PROCEDURAL": 0,
            "STARTPAUSED": 0,
            "FORCEISENVIRONMENT": 0,
            "COMPONENTS": [{
                    "__class": "JD_SongDescTemplate",
                    "MapName": self.song_data.userfriendly_id,
                    "JDVersion": 2017,
                    "OriginalJDVersion": 2017,
                    "Artist": self.song_data.artist,
                    "DancerName": "Unknown Dancer",
                    "Title": "CAN'T STOP THE FEELING!",
                    "Credits": "<< TO BE FILLED >>",
                    "PhoneImages": {
                        "cover": f"world/maps/{self.song_data.userfriendly_id.lower()}/menuart/textures/{self.song_data.userfriendly_id.lower()}_cover_phone.jpg",
                        "coach2": f"world/maps/{self.song_data.userfriendly_id.lower()}/menuart/textures/{self.song_data.userfriendly_id.lower()}_coach_2_phone.png",
                        "coach1": f"world/maps/{self.song_data.userfriendly_id.lower()}/menuart/textures/{self.song_data.userfriendly_id.lower()}_coach_1_phone.png"
                    },
                    "NumCoach": self.dancer_count,
                    "MainCoach": -1,
                    "Difficulty": 1,
                    "SweatDifficulty": 1,
                    "backgroundType": 0,
                    "LyricsType": 0,
                    "Tags": ["main"],
                    "Status": 3,
                    "LocaleID": 4294967295,
                    "MojoValue": 0,
                    "CountInProgression": 1,
                   "DefaultColors": {
                        "lyrics": [1, 1, 0, 0],
                        "theme": [1, 1, 1, 1],
                    },
                    "VideoPreviewPath": ""
                }
            ]
        }

__all__ = ["UbiArtMap"]
