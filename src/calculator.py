# src/calculator.py

EMISSION_FACTORS = {
    "electricity_kwh": 0.82,   # kg CO2 per kWh (India)
    "petrol_liter": 2.31,
    "diesel_liter": 2.68,
    "lpg_kg": 2.98,
    "cng_kg": 2.75,
    "bus_km": 0.05,
    "train_km": 0.01,
    "flight_km": 0.15,
    "veg_day": 2.0,
    "nonveg_day": 5.0,
    "plastic_kg": 6.0,
    "ewaste_kg": 20.0,
    "water_m3": 0.34
}

def calculate_electricity_co2(kwh):
    return kwh * EMISSION_FACTORS["electricity_kwh"]

def calculate_transport_co2(petrol=0, diesel=0, bus_km=0, train_km=0, flight_km=0):
    return (
        petrol * EMISSION_FACTORS["petrol_liter"]
        + diesel * EMISSION_FACTORS["diesel_liter"]
        + bus_km * EMISSION_FACTORS["bus_km"]
        + train_km * EMISSION_FACTORS["train_km"]
        + flight_km * EMISSION_FACTORS["flight_km"]
    )

def calculate_food_co2(diet_type, days=30):
    if diet_type.lower() == "veg":
        return days * EMISSION_FACTORS["veg_day"]
    else:
        return days * EMISSION_FACTORS["nonveg_day"]

def calculate_waste_co2(plastic_kg=0, ewaste_kg=0):
    return (
        plastic_kg * EMISSION_FACTORS["plastic_kg"]
        + ewaste_kg * EMISSION_FACTORS["ewaste_kg"]
    )

def calculate_water_co2(water_m3=0):
    return water_m3 * EMISSION_FACTORS["water_m3"]

def calculate_total_co2(user_inputs):
    electricity = calculate_electricity_co2(user_inputs.get("electricity_kwh", 0))
    transport = calculate_transport_co2(
        petrol=user_inputs.get("petrol_liters", 0),
        diesel=user_inputs.get("diesel_liters", 0),
        bus_km=user_inputs.get("bus_km", 0),
        train_km=user_inputs.get("train_km", 0),
        flight_km=user_inputs.get("flight_km", 0)
    )
    food = calculate_food_co2(user_inputs.get("diet", "veg"), user_inputs.get("days", 30))
    waste = calculate_waste_co2(
        plastic_kg=user_inputs.get("plastic_kg", 0),
        ewaste_kg=user_inputs.get("ewaste_kg", 0)
    )
    water = calculate_water_co2(user_inputs.get("water_m3", 0))

    monthly_total = electricity + transport + food + waste + water
    yearly_total = monthly_total * 12

    breakdown = {
        "electricity": round(electricity, 2),
        "transport": round(transport, 2),
        "food": round(food, 2),
        "waste": round(waste, 2),
        "water": round(water, 2),
        "monthly_total": round(monthly_total, 2),
        "yearly_total": round(yearly_total, 2)
    }

    percentages = {}
    for key in ["electricity", "transport", "food", "waste", "water"]:
        if monthly_total > 0:
            percentages[key] = round((breakdown[key] / monthly_total) * 100, 2)
        else:
            percentages[key] = 0

    highest_source = max(percentages, key=percentages.get)

    return breakdown, percentages, highest_source
