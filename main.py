import sys
import datetime
import pickle
import os
from property import Property
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.heap import MinHeap
from scraper import PropertyScraper
from filtering import PropertyFilter
from utils import calculate_distance_to_center, measure_time_complexity

class PriorityQueue:
    def __init__(self, comparator=None):
        self.heap = []
        self.size = 0
        self.comparator = comparator or (lambda x, y: x < y)

    def is_empty(self):
        return self.size == 0

    def peek(self):
        if self.size <= 0:
            return None
        return self.heap[0]

    def insert(self, item):
        self.heap.append(item)
        self.size += 1
        self._sift_up(self.size - 1)

    def extract(self):
        if self.size <= 0:
            return None
        top = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        if self.size > 0:
            self._sift_down(0)
        return top

    def _sift_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.comparator(self.heap[index], self.heap[parent]):
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < self.size and self.comparator(self.heap[left], self.heap[smallest]):
            smallest = left
        if right < self.size and self.comparator(self.heap[right], self.heap[smallest]):
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)

def main():
    print("Apartment Rental Finder - Riga (SS.com only)")
    print("====================================================================================================================")

    scraper = PropertyScraper()
    print("Getting rental data from SS.com...")
    ss_properties_rent = scraper.scrape_ss_com(max_price=1500) or []

    all_rent_properties = ss_properties_rent

    if not all_rent_properties:
        print("No rental properties found. Please check your internet connection or try again later.")
        sys.exit(1)
    else:
        print(f"Found {len(all_rent_properties)} rental properties.")

    print("Calculating distances to center...")
    for prop in all_rent_properties:
        distance, time_min = calculate_distance_to_center(prop.address)
        prop.distance_to_center = distance
        prop.time_to_center = time_min

    print("Removing duplicates...")
    unique_rent_properties = PropertyFilter.remove_duplicates(all_rent_properties)

    previous_properties = {}
    if os.path.exists('previous_rent_results.pkl'):
        try:
            with open('previous_rent_results.pkl', 'rb') as f:
                previous_properties = pickle.load(f)
        except Exception as e:
            print(f"Error reading previous results: {e}")

    new_properties = []
    for prop in unique_rent_properties:
        if prop.id not in previous_properties:
            new_properties.append(prop)
            previous_properties[prop.id] = datetime.datetime.now()

    try:
        with open('previous_rent_results.pkl', 'wb') as f:
            pickle.dump({prop.id: previous_properties.get(prop.id, datetime.datetime.now())
                         for prop in unique_rent_properties}, f)
    except Exception as e:
        print(f"Error saving results: {e}")

    print("Sorting properties by price...")
    print("\nMeasuring QuickSort performance:")
    sorted_rent_properties, quicksort_time = measure_time_complexity(
        PropertyFilter.sort_by_price_ascending, unique_rent_properties
    )

    print("\nBuilding Binary Search Tree for price-based searches:")
    rent_bst = BinarySearchTree()
    bst_build_time_start = datetime.datetime.now()
    for prop in sorted_rent_properties:
        rent_bst.insert(prop.price, prop)
    bst_build_time = (datetime.datetime.now() - bst_build_time_start).total_seconds()
    print(f"BST build time: {bst_build_time:.6f} seconds for {len(sorted_rent_properties)} properties")
    print(f"BST size: {rent_bst.size} nodes")

    print("\nBuilding Min-Heap for efficient minimum price lookups:")
    rent_min_heap = MinHeap()
    heap_build_time_start = datetime.datetime.now()
    for prop in sorted_rent_properties:
        rent_min_heap.insert(prop)
    heap_build_time = (datetime.datetime.now() - heap_build_time_start).total_seconds()
    print(f"Min-Heap build time: {heap_build_time:.6f} seconds")
    print(f"Min-Heap size: {rent_min_heap.size} elements")

    print("\nBuilding Priority Queue with custom comparator:")
    def custom_comparator(prop1, prop2):
        if prop1.utilities_included and not prop2.utilities_included:
            return True
        elif not prop1.utilities_included and prop2.utilities_included:
            return False
        else:
            return prop1.price < prop2.price

    rent_priority_queue = PriorityQueue(comparator=custom_comparator)
    pq_build_time_start = datetime.datetime.now()
    for prop in sorted_rent_properties:
        rent_priority_queue.insert(prop)
    pq_build_time = (datetime.datetime.now() - pq_build_time_start).total_seconds()
    print(f"Priority Queue build time: {pq_build_time:.6f} seconds")
    print(f"Priority Queue size: {rent_priority_queue.size} elements")

    print("\nRENTAL PROPERTY RESULTS:")
    print(f"Total found {len(sorted_rent_properties)} unique rental properties")

    if new_properties:
        print(f"\nFound {len(new_properties)} NEW properties since last check!")
        for i, prop in enumerate(new_properties, 1):
            print(f"\n=== NEW PROPERTY #{i} ===")
            print(prop)

    print("\nTop 5 cheapest rental properties (via QuickSort):")
    if sorted_rent_properties:
        for i in range(min(5, len(sorted_rent_properties))):
            print(f"\n{i+1}. {sorted_rent_properties[i]}")
    else:
        print("No rental properties found.")

    print("\nTop 3 cheapest rental properties (via Min-Heap):")
    if rent_min_heap.size > 0:
        for i in range(min(3, rent_min_heap.size)):
            prop = rent_min_heap.extract_min()
            print(f"\n{i+1}. {prop}")
    else:
        print("No rental properties found.")

    print("\nTop 3 properties by priority (utilities included first, then by price):")
    if rent_priority_queue.size > 0:
        for i in range(min(3, rent_priority_queue.size)):
            prop = rent_priority_queue.extract()
            print(f"\n{i+1}. {prop.price} EUR - {prop.title} ({'includes utilities' if prop.utilities_included else 'utilities not included'})")
    else:
        print("No rental properties found.")

    while True:
        print("\nMenu:")
        print("1. Show all rental properties (sorted by price)")
        print("2. Filter by price range (using BST)")
        print("3. Filter properties with utilities included")
        print("4. Show properties within certain distance from center")
        print("5. Show data structure and algorithm performance metrics")
        print("6. Exit")

        choice = input("Choose action (1-6): ")

        if choice == '1':
            for i, prop in enumerate(sorted_rent_properties, 1):
                print(f"\n{i}. {prop}")

        elif choice == '2':
            try:
                min_price = float(input("Minimum price: "))
                max_price = float(input("Maximum price: "))
                start_time = datetime.datetime.now()
                rent_in_range = rent_bst.find_range(min_price, max_price)
                search_time = (datetime.datetime.now() - start_time).total_seconds()
                print(f"BST range search execution time: {search_time:.6f} seconds")
                print(f"Found {len(rent_in_range)} properties in price range {min_price}-{max_price} EUR")
                for i, prop in enumerate(rent_in_range, 1):
                    print(f"\n{i}. {prop}")
            except ValueError:
                print("Please enter valid numbers for the price range.")

        elif choice == '3':
            included = input("Are utilities included? (y/n): ").lower() == 'y'
            start_time = datetime.datetime.now()
            filtered = PropertyFilter.filter_by_utilities_included(sorted_rent_properties, included)
            filter_time = (datetime.datetime.now() - start_time).total_seconds()
            print(f"Filter execution time: {filter_time:.6f} seconds")
            print(f"Found {len(filtered)} properties with utilities {'included' if included else 'not included'}")
            for i, prop in enumerate(filtered, 1):
                print(f"\n{i}. {prop}")

        elif choice == '4':
            try:
                max_distance = float(input("Maximum distance from center (km): "))
                start_time = datetime.datetime.now()
                close_to_center = PropertyFilter.filter_by_distance(sorted_rent_properties, max_distance)
                filter_time = (datetime.datetime.now() - start_time).total_seconds()
                print(f"Distance filter execution time: {filter_time:.6f} seconds")
                print(f"Found {len(close_to_center)} properties within {max_distance} km from center")
                for i, prop in enumerate(close_to_center, 1):
                    print(f"\n{i}. {prop}")
            except ValueError:
                print("Please enter a valid number for the distance.")

        elif choice == '5':
            print("\nData Structure and Algorithm Performance Metrics:")
            print("="*80)
            print(f"Number of rental properties: {len(sorted_rent_properties)}")
            print(f"QuickSort execution time: {quicksort_time:.6f} seconds")
            print(f"BST build time: {bst_build_time:.6f} seconds")
            print(f"Min-Heap build time: {heap_build_time:.6f} seconds")
            print(f"Priority Queue build time: {pq_build_time:.6f} seconds")
            print("="*80)

        elif choice == '6':
            print("Thank you for using the Apartment Rental Finder!")
            break

        else:
            print("Invalid choice, please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()