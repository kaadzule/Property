class Property:
    """Property class for rental real estate data"""

    def __init__(self, id, title, price, address, size, rooms, floor=None,
                 has_furniture=None, kitchen_equipment=None, bathroom=None,
                 utilities_included=None, source_url=None, portal=None,
                 published_date=None, has_parking=None, pets_allowed=None, min_rent_term=None):
        self.id = id
        self.title = title
        self.price = float(price)
        self.address = address
        self.size = size
        self.rooms = rooms
        self.floor = floor
        self.has_furniture = has_furniture
        self.kitchen_equipment = kitchen_equipment or []
        self.bathroom = bathroom
        self.utilities_included = utilities_included
        self.distance_to_center = None
        self.time_to_center = None
        self.source_url = source_url
        self.portal = portal
        self.published_date = published_date
        self.has_parking = has_parking
        self.pets_allowed = pets_allowed
        self.min_rent_term = min_rent_term

    def __str__(self):
        fields = [
            f"{self.title}",
            f"Price: {self.price:.2f} EUR/month" + (
                f" (Utilities {'included' if self.utilities_included else 'not included'})"
                if self.utilities_included is not None else ""
            ),
            f"Rooms: {self.rooms}",
            f"Address: {self.address}",
            f"Size: {self.size:.2f} m²",
            f"Floor: {self.floor}" if self.floor is not None else None,
            f"Furniture: {'Yes' if self.has_furniture else 'No'}" if self.has_furniture is not None else None,
            f"Kitchen equipment: {', '.join(self.kitchen_equipment)}" if self.kitchen_equipment else None,
            f"Bathroom: {self.bathroom}" if self.bathroom else None,
            f"Distance to center: {self.distance_to_center:.2f} km, {self.time_to_center} min by car"
                if self.distance_to_center is not None and self.time_to_center is not None else None,
            f"Parking: {'Yes' if self.has_parking else 'No'}" if self.has_parking is not None else None,
            f"Pets allowed: {'Yes' if self.pets_allowed else 'No'}" if self.pets_allowed is not None else None,
            f"Minimum rental term: {self.min_rent_term}" if self.min_rent_term else None,
            f"Published: {self.published_date}" if self.published_date else None,
            f"Link: {self.source_url}"
        ]
        return "\n".join(filter(None, fields))

    def text_format(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.address, self.size, self.rooms, self.price))

    def __eq__(self, other):
        if not isinstance(other, Property):
            return False
        return (
            self.address.lower() == other.address.lower()
            and abs(self.size - other.size) < 2
            and self.rooms == other.rooms
        )

    def __lt__(self, other):
        return self.price < other.price

    def __le__(self, other):
        return self.price <= other.price

    def __gt__(self, other):
        return self.price > other.price

    def __ge__(self, other):
        return self.price >= other.price