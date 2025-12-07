"""Live API test script."""

import requests
import json

BASE_URL = "http://localhost:8000"

print("🎵 Testing Species Counterpoint API\n")

# Test 1: Health check
print("1. Health Check...")
response = requests.get(f"{BASE_URL}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

# Test 2: Generate Cantus Firmus
print("2. Generate Cantus Firmus...")
cf_request = {
    "tonic": 0,
    "mode": "ionian",
    "length": 8,
    "voice_range": "alto",
    "seed": 42
}
response = requests.post(f"{BASE_URL}/api/generate-cantus-firmus", json=cf_request)
print(f"   Status: {response.status_code}")
cf_data = response.json()
cf_notes = [n["midi"] for n in cf_data["notes"]]
print(f"   CF Notes (MIDI): {cf_notes}\n")

# Test 3: Generate Counterpoint
print("3. Generate First Species Counterpoint...")
cp_request = {
    "tonic": 0,
    "mode": "ionian",
    "cf_notes": cf_notes,
    "cf_voice_range": "alto",
    "seed": 42
}
response = requests.post(f"{BASE_URL}/api/generate-counterpoint", json=cp_request)
print(f"   Status: {response.status_code}")
cp_data = response.json()
cp_notes = [n["midi"] for n in cp_data["cp_notes"]]
print(f"   CP Notes (MIDI): {cp_notes}")
print(f"   Violations: {len(cp_data['violations'])}\n")

# Test 4: Evaluate Counterpoint
print("4. Evaluate Counterpoint...")
eval_request = {
    "tonic": 0,
    "mode": "ionian",
    "cf_notes": cf_notes,
    "cp_notes": cp_notes
}
response = requests.post(f"{BASE_URL}/api/evaluate-counterpoint", json=eval_request)
print(f"   Status: {response.status_code}")
eval_data = response.json()
print(f"   Valid: {eval_data['is_valid']}")
print(f"   Violations: {len(eval_data['violations'])}\n")

print("✅ All API tests completed!")
print(f"\n📚 View full API docs at: {BASE_URL}/docs")
