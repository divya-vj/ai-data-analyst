print("Testing imports...")
print("Current directory:", __file__)

try:
    from config import APP_TITLE
    print("✅ config imported!")
except Exception as e:
    print(f"❌ config failed: {e}")

try:
    from data_loader import DataLoader
    print("✅ data_loader imported!")
except Exception as e:
    print(f"❌ data_loader failed: {e}")

try:
    from analyzer import DataAnalyzer
    print("✅ analyzer imported!")
except Exception as e:
    print(f"❌ analyzer failed: {e}")

print("Test complete!")