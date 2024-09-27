import math
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 100

class CelestialBody:
    def __init__(self, name, mass, radius, angular_velocity, moment_of_inertia_factor='0.4'):
        self.name = name
        self.mass = Decimal(mass)  # Mass in kg
        self.radius = Decimal(radius) * Decimal('1000')  # Radius in meters
        self.angular_velocity = Decimal(angular_velocity)  # Angular velocity in radians per second
        self.moment_of_inertia_factor = Decimal(moment_of_inertia_factor)

# Constants
GRAVITATIONAL_CONSTANT = Decimal('6.67430e-11')  # G in m³ kg⁻¹ s⁻²
SPEED_OF_LIGHT = Decimal('299792458')            # c in m/s

# Define celestial bodies
Sun = CelestialBody("Sun", "1.9885e30", "696340", "2.865e-6", '0.070')
Mercury = CelestialBody("Mercury", "3.3011e23", "2439.7", "1.240e-6", '0.346')
Venus = CelestialBody("Venus", "4.8675e24", "6051.8", "2.99e-7", '0.337')
Earth = CelestialBody("Earth", "5.97219e24", "6371", "7.2921150e-5", '0.3307')
Mars = CelestialBody("Mars", "6.4171e23", "3389.5", "7.088e-5", '0.366')
Jupiter = CelestialBody("Jupiter", "1.89813e27", "69911", "1.758e-4", '0.254')
Saturn = CelestialBody("Saturn", "5.68319e26", "58232", "1.637e-4", '0.220')
Uranus = CelestialBody("Uranus", "8.6810e25", "25362", "1.012e-4", '0.229')
Neptune = CelestialBody("Neptune", "1.02413e26", "24622", "1.083e-4", '0.228')
R136a1 = CelestialBody("R136a1", "4.4e32", "3885000", "0", '0.070')  # Approximate values

celestial_bodies = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, R136a1]

def calculate_angular_momentum(body):
    """
    Calculate the angular momentum J of a celestial body.
    J = I * omega
    where I = k * M * R^2 (moment of inertia)
    """
    I = body.moment_of_inertia_factor * body.mass * body.radius**2
    J = I * body.angular_velocity
    return J

def calculate_specific_angular_momentum(body):
    """
    Calculate specific angular momentum a = J / (M * c)
    """
    J = calculate_angular_momentum(body)
    a = J / (body.mass * SPEED_OF_LIGHT)
    return a

def calculate_time_dilation_factor(body, r):
    """
    Calculate time dilation factor using the weak-field approximation.
    """
    G = GRAVITATIONAL_CONSTANT
    c = SPEED_OF_LIGHT
    M = body.mass

    # Gravitational potential
    phi = -G * M / r
    gravitational_factor = 1 + phi / c**2

    # Kinetic energy per unit mass
    if r > body.radius:
        # For a satellite in orbit
        v = (G * M / r).sqrt()
    else:
        # For a point on the surface
        v = body.angular_velocity * r
    kinetic_factor = 1 - (v**2) / (2 * c**2)

    time_dilation_factor = gravitational_factor * kinetic_factor

    return time_dilation_factor

def format_time_difference(time_diff):
    """
    Convert the time difference into an appropriate time unit for readability.
    """
    abs_diff = abs(time_diff)
    if abs_diff >= Decimal('86400'):
        formatted = f"{abs_diff / Decimal('86400'):.6f} days"
    elif abs_diff >= Decimal('3600'):
        formatted = f"{abs_diff / Decimal('3600'):.6f} hours"
    elif abs_diff >= Decimal('60'):
        formatted = f"{abs_diff / Decimal('60'):.6f} minutes"
    elif abs_diff >= Decimal('1'):
        formatted = f"{abs_diff:.6f} seconds"
    elif abs_diff >= Decimal('1e-3'):
        formatted = f"{(abs_diff * Decimal('1e3')):.6f} milliseconds"
    elif abs_diff >= Decimal('1e-6'):
        formatted = f"{(abs_diff * Decimal('1e6')):.6f} microseconds"
    elif abs_diff >= Decimal('1e-9'):
        formatted = f"{(abs_diff * Decimal('1e9')):.6f} nanoseconds"
    else:
        formatted = f"{(abs_diff * Decimal('1e12')):.6f} picoseconds"
    return formatted

def get_valid_number(prompt, default=None):
    """
    Prompt the user for a number, optionally with a default value.
    """
    while True:
        user_input = input(prompt)
        if not user_input.strip():
            if default is not None:
                return Decimal(default)
            else:
                print("Input cannot be empty.")
                continue
        try:
            value = Decimal(user_input)
            return value
        except:
            print("Invalid input. Please enter a valid number.")

# Main Program Starts Here
# Collect user input
time_interval = get_valid_number("Time interval (in hours): ") * Decimal('3600')  # Convert hours to seconds

# First frame of reference
print("\nFirst frame of reference")
distance_from_surface_1 = get_valid_number("Distance from surface (in km): ") * Decimal('1000')  # Convert km to meters

print("\nPreset available:")
print("Custom [0]")
for idx, body in enumerate(celestial_bodies, start=1):
    print(f"{body.name} [{idx}]")
celestial_body_choice = input("Enter '0' for Custom or choose a preset: ")

if celestial_body_choice == "0":
    # User-defined celestial body
    custom_mass = get_valid_number("Enter mass for Custom (in kg): ")
    custom_radius = get_valid_number("Enter radius for Custom (in km): ")
    angular_velocity = get_valid_number("Angular velocity (in radians per second): ")
    moment_of_inertia_factor = get_valid_number("Moment of inertia factor k (default 0.4): ", default='0.4')
    selected_body_1 = CelestialBody("Custom", custom_mass, custom_radius, angular_velocity, moment_of_inertia_factor)
else:
    # Preset celestial body
    try:
        selected_body_1 = celestial_bodies[int(celestial_body_choice) - 1]
    except (IndexError, ValueError):
        print("Invalid selection. Exiting.")
        exit()

total_distance_1 = selected_body_1.radius + distance_from_surface_1

# Calculate specific angular momentum for the first frame (even if not used yet)
specific_angular_momentum_1 = calculate_specific_angular_momentum(selected_body_1)

# Calculate time dilation factor for the first frame
total_time_dilation_1 = calculate_time_dilation_factor(selected_body_1, total_distance_1)

# Second frame of reference
print("\nSecond frame of reference")
distance_from_surface_2 = get_valid_number("Distance from surface (in km): ") * Decimal('1000')  # Convert km to meters

celestial_body_choice = input("Enter '0' for Custom or choose a preset: ")

if celestial_body_choice == "0":
    # User-defined celestial body
    custom_mass = get_valid_number("Enter mass for Custom (in kg): ")
    custom_radius = get_valid_number("Enter radius for Custom (in km): ")
    angular_velocity = get_valid_number("Angular velocity (in radians per second): ")
    moment_of_inertia_factor = get_valid_number("Moment of inertia factor k (default 0.4): ", default='0.4')
    selected_body_2 = CelestialBody("Custom", custom_mass, custom_radius, angular_velocity, moment_of_inertia_factor)
else:
    # Preset celestial body
    try:
        selected_body_2 = celestial_bodies[int(celestial_body_choice) - 1]
    except (IndexError, ValueError):
        print("Invalid selection. Exiting.")
        exit()

total_distance_2 = selected_body_2.radius + distance_from_surface_2

# Calculate specific angular momentum for the second frame (even if not used yet)
specific_angular_momentum_2 = calculate_specific_angular_momentum(selected_body_2)

# Calculate time dilation factor for the second frame
total_time_dilation_2 = calculate_time_dilation_factor(selected_body_2, total_distance_2)

# Calculate time difference between the two frames
time_difference = time_interval * (total_time_dilation_2 - total_time_dilation_1)

# Format and display the time difference
time_diff_formatted = format_time_difference(time_difference)
print("")
print(f"{time_interval / Decimal('3600')} hours in the first frame of reference is {time_diff_formatted} {'slower' if time_difference < 0 else 'faster'} in the second frame of reference.")
