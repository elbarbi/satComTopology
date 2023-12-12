from src.sat_com_model.exception import InterSatelliteConnectionError, GroundStationConnectionError, \
    UserTerminalConnectionError, SimulationContextError


class SpatialPoint:
    """
    This is the lower element of the stack. Every element in the topology has a position
    """
    longitude: float
    latitude: float
    altitude: float

    def get_position(self) -> (float, float, float):
        return self.longitude, self.latitude, self.altitude


class TopologyObject(SpatialPoint):
    """
    Any Object in the topology
    """
    object_name: str
    id: int


class OrbitalObject(TopologyObject):
    """
    Any object in orbit
    """
    tle: str
    orbital_object_id: int


class Satellite(OrbitalObject):
    satellite_name: str
    satellite_id: int


class GroundObject(TopologyObject):
    pass


class GroundStation(GroundObject):
    ground_station_id: int
    city: str


class UserTerminal(GroundObject):
    user_id: int
    user_name: str


class Link:
    """
    This is the communication Link
    Todo: maybe we should directly connect interface here
    """
    source: TopologyObject
    destination: TopologyObject

    def connect(self, source: TopologyObject, destination: TopologyObject):
        self.source = source
        self.destination = destination


class InterSatelliteLink(Link):
    def connect(self, source: TopologyObject, destination: TopologyObject):
        object_are_both_satellites = source is Satellite and destination is Satellite
        if not object_are_both_satellites:
            raise InterSatelliteConnectionError()

        super().connect(source, destination)


class GroundStationLink(Link):
    def connect(self, source: TopologyObject, destination: TopologyObject):
        object_source_is_a_gsl_and_destination_a_satellite = source is GroundStation and destination is Satellite
        object_source_is_a_satellite_and_destination_a_gsl = source is GroundStation and destination is Satellite

        cant_connect = (not object_source_is_a_gsl_and_destination_a_satellite and
                        not object_source_is_a_satellite_and_destination_a_gsl)

        if cant_connect:
            raise GroundStationConnectionError()

        super().connect(source, destination)


class UserTerminalLink(Link):
    def connect(self, source: TopologyObject, destination: TopologyObject):
        object_source_is_an_user_and_destination_a_satellite = source is UserTerminal and destination is Satellite
        object_source_is_a_satellite_and_destination_an_user = source is GroundStation and destination is UserTerminal

        cant_connect = (not object_source_is_an_user_and_destination_a_satellite and
                        not object_source_is_a_satellite_and_destination_an_user)

        if cant_connect:
            raise UserTerminalConnectionError()


class Simulation:
    available_id_index: int = 0

    topology_objects: list[TopologyObject]

    connection_links: list[Link]

    def request_an_id(self):
        attributed_id = self.available_id_index
        self.available_id_index += 1

        return attributed_id


def create_satellite(simulation_context: Simulation, satellite_name, satellite_id) -> Satellite:
    """
    Create a satellite with parameters
    todo: check what we have to put inside a satellite object
    :param simulation_context: REQUIRED SIMULATION, very important to identify our future satellite.
    :param satellite_name: Name of the satellite
    :param satellite_id: Identifier of the satellite
    :return:
    """
    if simulation_context is None:
        raise SimulationContextError()

    created_satellite = Satellite()

    created_satellite.satellite_id = satellite_id
    created_satellite.satellite_name = satellite_name
    created_satellite.id = simulation_context.request_an_id()

    return created_satellite


def create_ground_station(simulation_context: Simulation, ground_station_id: int, city: str) -> GroundStation:
    """
    Create a ground station
    :param simulation_context: REQUIRED SIMULATION, very important to identify our future satellite.
    :param ground_station_id: identifier of the ground station
    :param city: position of the ground station (closest city)
    :return:
    """
    if simulation_context is None:
        raise SimulationContextError()

    created_ground_station = GroundStation()
    created_ground_station.id = simulation_context.request_an_id()
    created_ground_station.city = city
    created_ground_station.ground_station_id = ground_station_id

    return created_ground_station


def create_user_terminal(simulation_context: Simulation, user_id, username) -> UserTerminal:
    """
    Create a user terminal
    :param username: username
    :param simulation_context: REQUIRED SIMULATION, very important to identify our future satellite.
    :param user_id: identifier of the user
    :return:
    """
    if simulation_context is None:
        raise SimulationContextError()

    created_user = UserTerminal()
    created_user.id = simulation_context.request_an_id()
    created_user.user_name = username
    created_user.user_id = user_id

    return created_user
