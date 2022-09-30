import os
import json
from JXDanceAPI import JXDanceAPI
from SongData import SongData
from ARData import ARData
from UbiArtMap import UbiArtMap


def create_output_folder() -> None:
    try:
        os.mkdir("output/")
    except:
        pass


def ask_material_number() -> int:
    return int(input("Material number (ID in LocalClassicDance/LocalChildrenDance): "))


def main() -> None:
    create_output_folder()
    
    print("jxd2ubiart - A simple script for converting Keep Dance AR data to UbiArt's Just Dance tape\n")
    print("This is free and unencumbered software released into the public domain.\n")

    material_number = ask_material_number()

    jxd_api = JXDanceAPI()
    
    raw_song_data = jxd_api.get_dance_info(material_number)
    raw_ar_data = jxd_api.get_ar_data(raw_song_data["id"])
    
    song_data = SongData(raw_song_data)
    ar_data = ARData(raw_ar_data)

    ubiart_map = UbiArtMap(song_data.generate_beats(), song_data)
    for pictogram in ar_data.pictograms:
        ubiart_map.add_pictogram_clip(pictogram)

    with open(f"output/{song_data.userfriendly_id}_songdesc.tpl.ckd", "w") as f:
        json.dump(ubiart_map.generate_song_description(), f)

    with open(f"output/{song_data.userfriendly_id}_tml_dance.dtape.ckd", "w") as f:
        json.dump(ubiart_map.generate_dance_tape(), f)

    with open(f"output/{song_data.userfriendly_id}_musictrack.tpl.ckd", "w") as f:
        json.dump(ubiart_map.generate_musictrack(), f)


if __name__ == "__main__":
    main()
