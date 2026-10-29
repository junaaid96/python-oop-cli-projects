from abc import ABC, abstractmethod


class Ride_Sharing:
    def __init__(self, company_name) -> None:
        self.company_name = company_name
        self.riders = []
        self.drivers = []

    def add_rider(self, rider):
        self.riders.append(rider)

    def add_driver(self, driver):
        self.drivers.append(driver)

    def __repr__(self) -> str:
        return f"{self.company_name} has {len(self.drivers)} drivers and {len(self.riders)} riders"


class User(ABC):
    def __init__(self, name, email, nid) -> None:
        self.name = name
        self.email = email
        self._nid = nid

    @abstractmethod
    def display_profile(self):
        raise NotImplementedError


class Driver(User):
    def __init__(self, name, email, nid, current_location) -> None:
        super().__init__(name, email, nid)
        self.current_location = current_location

    def display_profile(self):
        return f"Driver's name: {self.name} and email: {self.email}"


class Rider(User):
    def __init__(self, name, email, nid, current_location) -> None:
        super().__init__(name, email, nid)
        self.current_ride = False
        self.current_location = current_location

    def display_profile(self):
        return f"Rider's name: {self.name} and email: {self.email}"

    def ride_request(self, ride_sharing, destination):
        if self.current_ride == False:
            rm = Ride_Matching(ride_sharing.drivers)
            res = rm.has_driver(self, destination)
            self.current_ride = True
            return f"Ride Details: {res}"


class Ride:
    def __init__(self, start_location, end_location) -> None:
        self.start_location = start_location
        self.end_location = end_location
        self.driver = None
        self.rider = None

    def start_drive():
        pass

    def end_ride():
        pass

    def __repr__(self) -> str:
        return f"Ride started from {self.start_location} to {self.end_location}"


class Ride_Matching:
    def __init__(self, drivers) -> None:
        self.drivers = drivers

    def has_driver(self, rider, destination):
        if len(self.drivers) > 0:
            ride = Ride(rider.current_location, destination)
            return ride
        else:
            return "Driver Not Found!"


uber = Ride_Sharing("Uber")
abid = Driver("Abid", "abid@gmail.com", 12345, "Kajir Dewri 1")
rakib = Rider("Rakib", "rakib@gmail.com", 67890, "Kajir Dewri 2")

driver = uber.add_driver(abid)
rider = uber.add_rider(rakib)

print(rakib.ride_request(uber, "Chawkbazar"))
