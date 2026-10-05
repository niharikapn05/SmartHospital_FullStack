import time

from algorithms import binary_search, linear_search
from hospital import Hospital


def create_test_data(size: int) -> Hospital:
    hospital = Hospital()

    # Add doctors
    for i in range(size):
        hospital.add_doctor(
            f"Doctor {i}",
            "Cardiologist"
        )

    # Add patients
    for i in range(size):
        hospital.register_patient(
            f"Patient {i}",
            20 + (i % 50),
            f"900000{i:04d}"
        )

    return hospital


def measure_linear_search(hospital: Hospital) -> float:
    start = time.perf_counter()

    linear_search(
        hospital.doctors,
        lambda doctor: doctor.name == "Doctor 999"
    )

    end = time.perf_counter()

    return end - start


def measure_binary_search(hospital: Hospital) -> float:
    doctors = sorted(
        hospital.doctors,
        key=lambda doctor: doctor.name
    )

    start = time.perf_counter()

    binary_search(
        doctors,
        "Doctor 999",
        lambda doctor: doctor.name
    )

    end = time.perf_counter()

    return end - start


def measure_queue_operation(hospital: Hospital) -> float:
    start = time.perf_counter()

    hospital.call_next_patient()

    end = time.perf_counter()

    return end - start


def main() -> None:
    print("===================================")
    print(" SMART HOSPITAL PERFORMANCE TEST")
    print("===================================")

    size = 1000

    print(f"\nCreating {size} doctors and patients...")
    hospital = create_test_data(size)

    print("Test data created successfully.")

    linear_time = measure_linear_search(hospital)
    binary_time = measure_binary_search(hospital)
    queue_time = measure_queue_operation(hospital)

    print("\n--- Performance Results ---")

    print(
        f"Linear Search Time : "
        f"{linear_time:.8f} seconds"
    )

    print(
        f"Binary Search Time : "
        f"{binary_time:.8f} seconds"
    )

    print(
        f"Queue Operation Time: "
        f"{queue_time:.8f} seconds"
    )

    print("\n--- Complexity Analysis ---")

    print("Linear Search  : O(n)")
    print("Binary Search  : O(log n)")
    print("Priority Queue : O(log n) for insertion/removal")
    print("Queue Peek     : O(1)")

    print("\nPerformance test completed successfully.")


if __name__ == "__main__":
    main()