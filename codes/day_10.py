from datetime import datetime

timestamp_microseconds = 1687041666339625
timestamp_seconds = timestamp_microseconds / 1e6  # Convert microseconds to seconds

# Create a datetime object
dt_object = datetime.utcfromtimestamp(timestamp_seconds)

# Format the datetime object as a string
formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")

print(formatted_time)
