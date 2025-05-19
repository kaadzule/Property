class PropertyFilter:
    """Class for working with property filtering"""

    @staticmethod
    def filter_by_price_range(properties, min_price=0, max_price=float('inf')):
        """Filter properties by price range"""
        return [prop for prop in properties if min_price <= prop.price <= max_price]

    @staticmethod
    def filter_by_utilities_included(properties, included=True):
        """Filter properties by whether utilities are included"""
        return [prop for prop in properties if prop.utilities_included == included]

    @staticmethod
    def filter_by_district(properties, district_list):
        """Filter properties by city district"""
        result = []
        for prop in properties:
            for district in district_list:
                if district.lower() in prop.address.lower():
                    result.append(prop)
                    break
        return result

    @staticmethod
    def filter_by_distance(properties, max_distance):
        """Filter properties by distance to center"""
        return [prop for prop in properties if prop.distance_to_center and prop.distance_to_center <= max_distance]

    @staticmethod
    def filter_by_rooms(properties, min_rooms, max_rooms=float('inf')):
        """Filter properties by number of rooms"""
        return [prop for prop in properties if min_rooms <= prop.rooms <= max_rooms]

    @staticmethod
    def filter_by_furniture(properties, has_furniture=True):
        """Filter properties by furniture"""
        return [prop for prop in properties if prop.has_furniture == has_furniture]

    @staticmethod
    def filter_by_pets_allowed(properties, allowed=True):
        """Filter properties by pet allowance"""
        return [prop for prop in properties if prop.pets_allowed == allowed]

    @staticmethod
    def filter_by_parking(properties, available=True):
        """Filter properties by parking availability"""
        return [prop for prop in properties if prop.has_parking == available]

    @staticmethod
    def filter_by_publish_date(properties, target_date):
        """Filter properties by published date (ISO format string)"""
        return [prop for prop in properties if prop.published_date == target_date]

    @staticmethod
    def sort_by_price_ascending(properties):
        """Sort properties by price in ascending order using QuickSort"""
        if not properties:
            return []

        return PropertyFilter._quick_sort(properties.copy(), 0, len(properties) - 1)

    @staticmethod
    def _quick_sort(arr, low, high):
        """QuickSort algorithm implementation"""
        if low < high:
            pivot_index = PropertyFilter._partition(arr, low, high)
            PropertyFilter._quick_sort(arr, low, pivot_index - 1)
            PropertyFilter._quick_sort(arr, pivot_index + 1, high)
        return arr

    @staticmethod
    def _partition(arr, low, high):
        """Partition array around pivot element"""
        pivot = arr[high].price
        i = low - 1
        for j in range(low, high):
            if arr[j].price <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    @staticmethod
    def remove_duplicates(properties):
        """Remove duplicate properties, keeping the cheapest one"""
        if not properties:
            return []

        unique_properties = {}

        for prop in properties:
            prop_hash = hash(prop)
            if prop_hash in unique_properties:
                if prop.price < unique_properties[prop_hash].price:
                    unique_properties[prop_hash] = prop
                elif prop.price == unique_properties[prop_hash].price:
                    existing_prop = unique_properties[prop_hash]
                    existing_prop.portal += f", {prop.portal}"
                    existing_prop.source_url += f", {prop.source_url}"
            else:
                unique_properties[prop_hash] = prop

        return list(unique_properties.values())