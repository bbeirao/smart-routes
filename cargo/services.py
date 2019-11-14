# Python 3.7
from loadsmart import settings
import csv
import requests
import logging

logger = logging.getLogger(__name__)


class FileService:

    def run(self, file):
        file_path = settings.FILE_DIR
        try:
            with open(file_path + file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                file_info = []
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        file_info.append(row)
                        line_count += 1
            return file_info
        except FileNotFoundError:
            logger.error("File not found error! Verify if file exists.")
            raise FileNotFoundError
        except IOError:
            logger.error("File reading error!")
            raise IOError


class DeliveryService:

    def __init__(self):
        self.api_key = 'AIzaSyCeWKMOb4DcNBKkTyJKM8vSYxDVnQPlS3U'
        self.maps_url = 'https://maps.googleapis.com' \
                        '/maps/api/distancematrix/json?units=imperial&'
        self.delivery_list = []
        self.unprocessed_list = []

    def run(self, cargos, trucks):
        logger.info("Start processing")
        self.trucks = trucks
        try:
            for current_cargo in cargos:
                self.truck_pickup = 0
                self.distance = 0
                cargo = {}
                trucks_info = []
                for truck in trucks:
                    all_trucks_info = self.get_distance(truck,
                                                        current_cargo,
                                                        trucks_info)
                cargo = self.build_cargo_dict(cargo,
                                              current_cargo,
                                              all_trucks_info)
                self.build_routes(cargo, self.delivery_list)
        except (Exception, TypeError) as e:
            error_message = "File reading error!"
            logger.error(error_message, e)

        while len(self.unprocessed_list) > 0:
            logger.info("Repeat trucks cargos reprocess")
            self.unprocessed_list = self.process_cargos(self.unprocessed_list)

        return self.build_final_list(self.delivery_list)

    @staticmethod
    def build_final_list(delivery_list):
        final_list = []
        final_list_reduced = []
        for delivery in delivery_list:
            # json with complete information
            final_data = {}
            final_data['cargo'] = delivery['cargo']
            final_data['truck'] = delivery['pickup']['truck']
            final_list.append(final_data)
            # reduced json information
            final_data_reduced = {}
            final_data_reduced['cargo'] = delivery['cargo'][0]
            final_data_reduced['truck'] = delivery['pickup']['truck'][0]
            final_list_reduced.append(final_data_reduced)
        return final_list, final_list_reduced

    def build_cargo_dict(self, cargo, current_cargo, all_trucks_info):
        cargo['cargo'] = current_cargo
        cargo['all_trucks_info'] = all_trucks_info
        cargo['pickup'] = self.best_distance(all_trucks_info)
        return cargo

    def get_distance(self, truck, current_cargo, trucks_info):
        route_info = {}
        api_response = self.get_distance_maps(self.maps_url,
                                              self.api_key,
                                              truck, current_cargo)
        distance = self.get_distance_info(api_response)
        route_info['truck'] = truck
        route_info['distance'] = distance
        trucks_info.append(route_info)
        return trucks_info

    def build_routes(self, new_cargo, saved_delivery_list):
        truck = new_cargo['pickup']['truck']
        if any(truck == delivery['pickup']['truck']
               for delivery in saved_delivery_list):
            self.process_repetead_truck(new_cargo, truck, saved_delivery_list)
        else:
            self.delivery_list.append(new_cargo)

    def process_repetead_truck(self, new_cargo, truck, saved_delivery_list):
        for delivery in saved_delivery_list:
            new_cargo_distance = new_cargo['pickup']['distance']
            saved_list_distance = delivery['pickup']['distance']
            if truck == delivery['pickup']['truck']:
                if new_cargo_distance < saved_list_distance:
                    cargo_unprocessed = self.build_unprocessed_cargo(delivery)
                    self.unprocessed_list.append(cargo_unprocessed)
                    self.delivery_list.append(new_cargo)
                    self.delivery_list.remove(delivery)
                else:
                    cargo_unprocessed = self.build_unprocessed_cargo(new_cargo)
                    self.unprocessed_list.append(cargo_unprocessed)

    @staticmethod
    def build_unprocessed_cargo(cargo_data):
        cargo_unprocessed = {}
        cargo_unprocessed['cargo'] = cargo_data['cargo']
        cargo_unprocessed['all_trucks_info'] = cargo_data['all_trucks_info']
        cargo_unprocessed['pickup'] = cargo_data['pickup']
        return cargo_unprocessed

    @staticmethod
    def get_distance_info(api_response):
        return api_response['rows'][0]['elements'][0]['distance']['value']

    def process_cargos(self, unprocessed_cargo_list):
        self.truck_pickup = 0
        self.distance = 0
        for unprocessed in unprocessed_cargo_list:
            cargo = {}
            trucks_to_process = self.exclude_truck_processed(unprocessed)
            cargo = self.build_cargo_dict(cargo,
                                          unprocessed['cargo'],
                                          trucks_to_process)
            self.build_unprocessed_routes(cargo, self.delivery_list)
            self.unprocessed_list.remove(unprocessed)
        return self.unprocessed_list

    @staticmethod
    def exclude_truck_processed(unprocessed_cargos_list):
        duplicated_cargo_info = unprocessed_cargos_list['pickup']
        all_trucks_info = unprocessed_cargos_list['all_trucks_info']
        return [i for i in all_trucks_info if not (i == duplicated_cargo_info)]

    def build_unprocessed_routes(self, cargo, saved_delivery_list):
        truck = cargo['pickup']['truck']
        if any(truck == delivery['pickup']['truck']
               for delivery in saved_delivery_list):
            self.process_repetead(cargo, truck, saved_delivery_list)
        else:
            self.delivery_list.append(cargo)

    def process_repetead(self, cargo, truck, saved_delivery_list):
        for saved_delivery in saved_delivery_list:
            cargo_distance = cargo['pickup']['distance']
            delivery_distance = saved_delivery['pickup']['distance']
            if truck == saved_delivery['pickup']['truck']:
                if cargo_distance < delivery_distance:
                    self.delivery_list.append(cargo)
                    self.unprocessed_list.remove(cargo)
                else:
                    cargo_unprocessed = self.build_unprocessed_cargo(cargo)
                    self.unprocessed_list.append(cargo_unprocessed)

    def best_distance(self, delivery):
        for route in delivery:
            self.verify_distance(route)
        return self.truck_pickup

    def verify_distance(self, route):
        distance = route['distance']
        if self.distance == 0:
            self.distance = distance
            self.truck_pickup = route
        elif distance < self.distance:
            self.distance = distance
            self.truck_pickup = route

    def get_distance_maps(self, maps_url, api_key, truck, cargo_origin):
        try:
            truck_lat = truck[3]
            truck_long = truck[4]
            cargo_lat = cargo_origin[3]
            cargo_long = cargo_origin[4]
            logger.info("Distance check with Google API")
            resp = requests.get(maps_url +
                                'origins=' + truck_lat + ',' + truck_long +
                                '&destinations=' + cargo_lat + ',' + cargo_long +
                                '&key=' + api_key)
            return resp.json()
        except ConnectionError:
            logger.error('Error Connecting.')
            raise ConnectionError
        except IOError:
            logger.error('IOError Error. Verify Api Url.')
            raise IOError
        except TypeError:
            logger.error('TypeError Error. Verify Params.')
            raise TypeError
