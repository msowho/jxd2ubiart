import requests
from enum import Enum


class JXDanceAPI:
    """
    Simple wrapper to Keep Dance RESTful API.

    Used for getting song information & AR data.
    """

    def __init__(self) -> None:
        """Constructor"""
        self.session = requests.Session()

        self.api_url = "http://api.jxdance.cn"
        self.endpoints = {
            "ask_ar_dance_detail": "/dance/material/detailExtend?materialId={0}",
            "ask_dance_info_by_material_no": "/dance/material/detail?materialNo={0}"
        }

    def get_dance_info(self, material_number: int):
        """Returns a map information."""
        request_url = self.api_url + self.endpoints["ask_dance_info_by_material_no"].format(material_number)
        
        with self.session.get(request_url) as r:
            response_body = r.json()

            assert r.status_code == 200 # Response status code ALWAYS 200
            assert response_body["data"] != None and response_body["code"] == 0

            return response_body["data"]

    def get_ar_data(self, material_id: int):
        """Returns AR data."""
        request_url = self.api_url + self.endpoints["ask_ar_dance_detail"].format(material_id)
        
        with self.session.get(request_url) as r:
            response_body = r.json()

            assert r.status_code == 200 # Response status code ALWAYS 200
            assert response_body["data"] != None and response_body["code"] == 0

            return response_body["data"]
