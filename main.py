import math
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 10000

class CelestialBody:
    def __init__(self, name, mass, radius, angular_velocity, moment_of_inertia_factor=Decimal('0.4')):
        self.name = name
        self.mass = Decimal(mass)  # Mass in kg
        self.radius = Decimal(radius) * Decimal('1000')  # Convert radius from km to meters
        self.angular_velocity = Decimal(angular_velocity)  # Angular velocity in radians per second
        self.moment_of_inertia_factor = Decimal(moment_of_inertia_factor)

# Constants
GRAVITATIONAL_CONSTANT = Decimal('6.67430e-11')  # Gravitational constant G in m^3 kg^-1 s^-2
SPEED_OF_LIGHT = Decimal('299792458')            # Speed of light c in m/s

# Define preset celestial bodies with angular velocities and moment of inertia factors
Sun = CelestialBody("Sun", "1.9885e30", "696340", "2.865e-6", moment_of_inertia_factor='0.070')
Mercury = CelestialBody("Mercury", "3.3011e23", "2439.7", "1.240e-6", moment_of_inertia_factor='0.346')
Venus = CelestialBody("Venus", "4.8675e24", "6051.8", "2.99e-7", moment_of_inertia_factor='0.337')
Earth = CelestialBody("Earth", "5.97219e24", "6371", "7.2921150e-5", moment_of_inertia_factor='0.3307')
Mars = CelestialBody("Mars", "6.4171e23", "3389.5", "7.088e-5", moment_of_inertia_factor='0.366')
Jupiter = CelestialBody("Jupiter", "1.89813e27", "69911", "1.758e-4", moment_of_inertia_factor='0.254')
Saturn = CelestialBody("Saturn", "5.68319e26", "58232", "1.637e-4", moment_of_inertia_factor='0.220')
Uranus = CelestialBody("Uranus", "8.6810e25", "25362", "1.012e-4", moment_of_inertia_factor='0.229')
Neptune = CelestialBody("Neptune", "1.02413e26", "24622", "1.083e-4", moment_of_inertia_factor='0.228')
R136a1 = CelestialBody("R136a1", "4.4e32", "3885000", "0", moment_of_inertia_factor='0.070')  # Mass and radius approximate

celestial_bodies = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, R136a1]

def calculate_angular_momentum(body):
    """
    Calculate the angular momentum J of a celestial body.
    J = I * omega
    where I = k * M * R^2 (moment of inertia)
    """
    moment_of_inertia = body.moment_of_inertia_factor * body.mass * body.radius**2
    angular_momentum = moment_of_inertia * body.angular_velocity
    return angular_momentum

def calculate_specific_angular_momentum(body):
    """
    Calculate specific angular momentum a = J / (M * c)
    """
    J = calculate_angular_momentum(body)
    a = J / (body.mass * SPEED_OF_LIGHT)
    return a

def kerr_metric_components(body, r):
    """
    Compute Kerr metric components at theta = pi/2 (equatorial plane)
    """
    G = GRAVITATIONAL_CONSTANT
    c = SPEED_OF_LIGHT
    M = body.mass
    a = calculate_specific_angular_momentum(body)
    # At theta = pi/2
    Sigma = r**2
    Delta = r**2 - (2 * G * M * r) / c**2 + a**2

    # Metric components
    g_tt = -(1 - (2 * G * M * r) / (r**2 * c**2))
    g_tphi = -(2 * G * M * a) / (r**2 * c)
    g_phiphi = r**2 + a**2 + (2 * G * M * a**2) / (r * c**2)

    return g_tt, g_tphi, g_phiphi

def calculate_orbital_angular_velocity(body, r):
    """
    Calculate orbital angular velocity omega for a circular equatorial orbit
    """
    G = GRAVITATIONAL_CONSTANT
    c = SPEED_OF_LIGHT
    M = body.mass
    a = calculate_specific_angular_momentum(body)
    # Compute omega using the exact Kerr metric formula for prograde orbits
    numerator = G * M * c * r - a * G * M
    denominator = c * r**3 - a**2 * G * M / c
    omega = numerator / denominator
    return omega

def calculate_time_dilation_factor(body, r):
    """
    Calculate time dilation factor d_tau/dt for an observer in a circular equatorial orbit
    """
    g_tt, g_tphi, g_phiphi = kerr_metric_components(body, r)
    omega = calculate_orbital_angular_velocity(body, r)
    # Compute the expression inside the square root
    expression = g_tt + 2 * g_tphi * omega + g_phiphi * omega**2
    if expression >= 0:
        # This indicates an error in calculations or an unphysical orbit
        raise ValueError("Invalid time-like interval: expression under square root is non-negative.")
    time_dilation_factor = Decimal(math.sqrt(-expression))
    return time_dilation_factor

# Function to calculate Schwarzschild radius
def calculate_schwarzschild_radius(body):
    """
    Calculate the Schwarzschild radius using:
    r_s = (2 * G * M) / c^2
    """
    return (2 * GRAVITATIONAL_CONSTANT * body.mass) / (SPEED_OF_LIGHT**2)

# Function to format time difference in a human-readable format
def format_time_difference(time_diff):
    """
    Convert the time difference into an appropriate time unit for readability.
    """
    abs_diff = abs(time_diff)
    if abs_diff >= Decimal('86400'):
        formatted = f"{abs(time_diff) / Decimal('86400'):.6f} days"
    elif abs_diff >= Decimal('3600'):
        formatted = f"{abs(time_diff) / Decimal('3600'):.6f} hours"
    elif abs_diff >= Decimal('60'):
        formatted = f"{abs(time_diff) / Decimal('60'):.6f} minutes"
    elif abs_diff >= Decimal('1'):
        formatted = f"{abs(time_diff):.6f} seconds"
    elif abs_diff >= Decimal('1e-3'):
        formatted = f"{abs(time_diff) * Decimal('1e3'):.6f} milliseconds"
    elif abs_diff >= Decimal('1e-6'):
        formatted = f"{abs(time_diff) * Decimal('1e6'):.6f} microseconds"
    elif abs_diff >= Decimal('1e-9'):
        formatted = f"{abs(time_diff) * Decimal('1e9'):.6f} nanoseconds"
    elif abs_diff >= Decimal('1e-12'):
        formatted = f"{abs(time_diff) * Decimal('1e12'):.6f} picoseconds"
    else:
        formatted = f"{abs(time_diff) * Decimal('1e15'):.6f} femtoseconds"  # For extremely small values
    return formatted

# Function to get valid numeric input from the user
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

# Check if within Schwarzschild radius
schwarzschild_radius_1 = calculate_schwarzschild_radius(selected_body_1)
if total_distance_1 <= schwarzschild_radius_1:
    print("Error: The total distance is within the Schwarzschild radius for the first frame of reference.")
    exit()

# Calculate time dilation factor for the first frame
try:
    total_time_dilation_1 = calculate_time_dilation_factor(selected_body_1, total_distance_1)
except ValueError as e:
    print(f"Error in time dilation calculation for the first frame: {e}")
    exit()

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

# Check if within Schwarzschild radius
schwarzschild_radius_2 = calculate_schwarzschild_radius(selected_body_2)
if total_distance_2 <= schwarzschild_radius_2:
    print("Error: The total distance is within the Schwarzschild radius for the second frame of reference.")
    exit()

# Calculate time dilation factor for the second frame
try:
    total_time_dilation_2 = calculate_time_dilation_factor(selected_body_2, total_distance_2)
except ValueError as e:
    print(f"Error in time dilation calculation for the second frame: {e}")
    exit()

# Calculate time difference between the two frames
time_difference = time_interval * (total_time_dilation_1 - total_time_dilation_2)

# Format and display the time difference
time_diff_formatted = format_time_difference(time_difference)
print("")
print(f"{time_interval / Decimal('3600')} hours in the first frame of reference is {time_diff_formatted} {'slower' if time_difference < 0 else 'faster'} in the second frame of reference.")
