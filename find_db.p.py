import os

found = []

for root, dirs, files in os.walk("C:/Users"):
    if "database.db" in files:
        found.append(os.path.join(root, "database.db"))

print("🔍 Знайдені файли database.db:\n")
for path in found:
    print(path)

print(f"\n✅ Усього знайдено: {len(found)}")
