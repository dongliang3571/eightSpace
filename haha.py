import os

folder = "uploaded"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
final = os.path.join(BASE_DIR, folder)

print final
