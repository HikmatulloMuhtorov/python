# scalene triangle: All sides have different lengths.
# Isoceles traingle: Two sides have the same length.
# Equilateral traingle: All sides are equal.

a = int(raw_input("The length of side a = "))
b = int(raw_input("The length of side b = "))
c = int(raw_input("The length of side c = "))

if a != b and b != c and a != c:
  print("This is a scalene triangle.")
elif a == b and b == c:
  print("This is an equilateral triangle.")
else:
  print("This is an isoceles triangle.")
