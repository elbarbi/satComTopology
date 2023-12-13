import unittest

from src.sat_com_model.exception import (
    GroundStationConnectionError,
    InterSatelliteConnectionError,
    UserTerminalConnectionError,
    ConnectionBetweenSameSatelliteForbiddenError,
)
from src.sat_com_model.model import (
    GroundStation,
    Satellite,
    GroundStationLink,
    UserTerminal,
    InterSatelliteLink,
    UserTerminalLink,
    Link,
    TopologyObject,
)


class TestLinks(unittest.TestCase):
    satellite: Satellite
    ground_station: GroundStation
    user_terminal = UserTerminal

    gsl_link: GroundStationLink
    isl_link: InterSatelliteLink
    user_link: UserTerminalLink

    def setUp(self):
        self.satellite = Satellite()
        self.ground_station = GroundStation()
        self.gsl_link = GroundStationLink()
        self.user_terminal = UserTerminal()
        self.isl_link = InterSatelliteLink()
        self.user_link = UserTerminalLink()

    def assert_can_establish_connection(
        self,
        link: Link,
        object_source: TopologyObject,
        object_destination: TopologyObject,
    ):
        link.connect(object_source, object_destination)
        self.assertTrue(
            link.source == object_source and link.destination == object_destination
        )

    def assert_cant_establish_connection(
        self,
        link: Link,
        expected_type_exception,
        object_source: TopologyObject,
        object_destination: TopologyObject,
    ):
        with self.assertRaises(expected_type_exception):
            link.connect(object_source, object_destination)

        assert link.source is None and link.destination is None

    def test_cant_establish_connection_between_same_object(self):
        single_topology_object = TopologyObject()
        link = Link()
        self.assert_cant_establish_connection(
            link,
            ConnectionBetweenSameSatelliteForbiddenError,
            single_topology_object,
            single_topology_object,
        )

    def test_bi_directional_connection_between_satellite_and_ground_station_using_gsl(
        self,
    ):
        self.assert_can_establish_connection(
            self.gsl_link, self.ground_station, self.satellite
        )
        self.assert_can_establish_connection(
            self.gsl_link, self.satellite, self.ground_station
        )

    def test_impossible_connection_between_satellites_using_gsl(self):
        second_satellite = Satellite()
        self.assert_cant_establish_connection(
            self.gsl_link,
            GroundStationConnectionError,
            self.satellite,
            second_satellite,
        )

    def test_impossible_connection_between_satellite_and_user_using_gsl(self):
        self.assert_cant_establish_connection(
            self.gsl_link,
            GroundStationConnectionError,
            self.satellite,
            self.user_terminal,
        )
        self.assert_cant_establish_connection(
            self.gsl_link,
            GroundStationConnectionError,
            self.user_terminal,
            self.satellite,
        )

    def test_satellites_cannot_connect_using_gsl_link(self):
        other_satellite = Satellite()

        self.assert_cant_establish_connection(
            self.gsl_link, GroundStationConnectionError, self.satellite, other_satellite
        )

    def test_user_and_satellite_cannot_connect_using_gsl_link(self):
        self.assert_cant_establish_connection(
            self.gsl_link,
            GroundStationConnectionError,
            self.satellite,
            self.user_terminal,
        )
        self.assert_cant_establish_connection(
            self.gsl_link,
            GroundStationConnectionError,
            self.user_terminal,
            self.satellite,
        )

    def test_satellite_can_connect_to_satellite_using_isl(self):
        other_satellite = Satellite()
        self.assert_can_establish_connection(
            self.isl_link, self.satellite, other_satellite
        )

    def test_satellite_cant_connect_to_gs_with_isl(self):
        self.assert_cant_establish_connection(
            self.isl_link,
            InterSatelliteConnectionError,
            self.satellite,
            self.ground_station,
        )
        self.assert_cant_establish_connection(
            self.isl_link,
            InterSatelliteConnectionError,
            self.ground_station,
            self.satellite,
        )

    def test_satellite_cant_connect_to_user_with_isl(self):
        self.assert_cant_establish_connection(
            self.isl_link,
            InterSatelliteConnectionError,
            self.satellite,
            self.user_terminal,
        )
        self.assert_cant_establish_connection(
            self.isl_link,
            InterSatelliteConnectionError,
            self.satellite,
            self.user_terminal,
        )

    def test_user_connect_with_satellite_using_utl(self):
        self.assert_can_establish_connection(
            self.user_link, self.user_terminal, self.satellite
        )
        self.assert_can_establish_connection(
            self.user_link, self.satellite, self.user_terminal
        )

    def test_gs_cant_connect_with_satellite_utl(self):
        self.assert_cant_establish_connection(
            self.user_link,
            UserTerminalConnectionError,
            self.ground_station,
            self.satellite,
        )
        self.assert_cant_establish_connection(
            self.user_link,
            UserTerminalConnectionError,
            self.satellite,
            self.ground_station,
        )


if __name__ == "__main__":
    unittest.main()
