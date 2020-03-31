alien_0 = {'color': 'green', 'points': 5}

print(alien_0['color'])
print(alien_0['points'])

new_points = alien_0['points']
print(f'You just earned {new_points} points!')

print(alien_0)

alien_0['x_position'] = 0
alien_0['y_position'] = 25

print(alien_0)

print("\n\nNew alien")
alien_0 = {}

alien_0['color'] = 'green'
alien_0['points'] = 5

print(alien_0)

print('\n\nNew alien')
alien_0 = {'color': 'green'}
print(f"The alien is {alien_0['color']}.")

alien_0['color'] = 'yellow'
print(f"The alien is now {alien_0['color']}.")

print('\n\nNew alien')

alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
print(f"Original position: {alien_0['x_position']}")

# Move alien to right
# Determine how far to move the alien based on current speed
if alien_0['speed'] == 'slow':
    x_increment = 1
elif alien_0['speed'] == 'medium':
    x_increment = 2
else:
    # This must be a fast alien
    x_increment = 3
# The new position is the old position plus the increment. 
alien_0['x_position'] = alien_0['x_position'] + x_increment

print(f"New position: {alien_0['x_position']}")

print("\n\nNew alien")
alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

del alien_0['points']
print(alien_0)

#alien_no_points.py
print('\n\nNew Alien')
alien_0 = {'color': 'green', 'points': 5}

point_value = alien_0.get('point', 'No point value assigned.')
print(point_value)