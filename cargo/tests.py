# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .services import FileService, DeliveryService

from django.conf import settings

import unittest
import json

fileService = FileService()
deliveryService = DeliveryService()
settings.configure()


class TestRequests(unittest.TestCase):
    if __name__ == "__main__":
        unittest.main()

    def setUp(self):
        self.cargo = fileService.run('cargo.csv')
        self.truck = fileService.run('trucks.csv')

    def test_process(self):
        delivery, _ = deliveryService.run(self.cargo, self.truck)
        with open('./files/final_list.json') as json_file:
            data = json.load(json_file)
            print(data)
        assert delivery == data

    def test_different_cargo(self):
        cargo = fileService.run('different_cargo.csv')
        delivery, _ = deliveryService.run(cargo, self.truck)
        with open('./files/different_final_list.json') as json_file:
            final_list = json.load(json_file)
        assert delivery == final_list

    def test_build_final_list(self):
        with open('./files/delivery.json') as json_file:
            list = json.load(json_file)
        with open('./files/different_final_list.json') as json_file:
            final_list_dict = json.load(json_file)
        final_list, _ = deliveryService.build_final_list(list)
        assert final_list == final_list_dict

    def test_cargo_file_error(self):
        with self.assertRaises(FileNotFoundError):
            fileService.run('cargo.cs')

    def test_truck_file_error(self):
        with self.assertRaises(FileNotFoundError):
            fileService.run('truck.cs')

    def test_url_error(self):
        api_key = 'AIzaSyCeWKMOb4DcNBKkTyJKM8vSYxDVnQPlS3U'
        maps_url = 'https://maps.googleapis.com'
        with self.assertRaises(IOError):
            deliveryService.get_distance_maps(maps_url, api_key, self.cargo[0], self.truck[0])
