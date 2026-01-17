from calculator import calculate_total_co2

user = {
    "electricity_kwh": 300,
    "petrol_liters": 40,
    "diet": "veg",
    "plastic_kg": 5,
    "water_m3": 10
}

breakdown, percentages, highest = calculate_total_co2(user)
print("Breakdown:", breakdown)
print("Percentages:", percentages)
print("Highest source:", highest)
