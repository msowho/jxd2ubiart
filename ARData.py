class Vector3:
    """3D vector"""

    def __init__(self, x: float, y: float, z: float) -> None:
        """Constructor"""
        self.x = x
        self.y = y
        self.z = z

class ARData:
    """AR data"""

    def __init__(self, raw_data: dict) -> None:
        """Constructor"""
        self.tracking_data = []
        self._init_tracking_data(raw_data["bodyData"])
        self._init_tracking_data(raw_data["bodyData2"])
        
        self.pictograms = []
        self._init_pictograms(raw_data["eventData"])

    def _init_tracking_data(self, body_data: str) -> None:
        for bone_element_string in body_data.splitlines():
            bone_element = {}

            time, vector_array_string = bone_element_string.split("#")

            bone_element["time"] = float(time)
            bone_element["vector_array"] = []

            for vector in vector_array_string.split("&"):
                x, y, z = vector.split(",")
                parsed_vector = Vector3(float(x), float(y), float(z))

                bone_element["vector_array"].append(parsed_vector)

            self.tracking_data.append(bone_element)

    def _init_pictograms(self, event_data: dict) -> None:
        for dance_logic in event_data["m_DanceLogicList"]:
            pictogram = {}

            pictogram["time"] = float(dance_logic["m_CurrentTime"])
            pictogram["texture_path"] = "Motion/{0}/{1}" \
                                        .format(event_data["m_DanceName"], dance_logic["m_ImageName"])

            self.pictograms.append(pictogram)
