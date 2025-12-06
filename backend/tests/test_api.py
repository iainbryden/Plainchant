"""Unit tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPI:
    """Tests for API endpoints."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_generate_cf(self):
        """Test CF generation endpoint."""
        response = client.post("/api/generate-cantus-firmus", json={
            "tonic": 0,
            "mode": "ionian",
            "length": 8,
            "voice_range": "soprano",
            "seed": 42
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "notes" in data
        assert len(data["notes"]) == 8
        assert data["voice_range"] == "soprano"
    
    def test_generate_counterpoint(self):
        """Test counterpoint generation endpoint."""
        # First generate CF
        cf_response = client.post("/api/generate-cantus-firmus", json={
            "tonic": 0,
            "mode": "ionian",
            "length": 8,
            "voice_range": "alto",
            "seed": 42
        })
        
        cf_notes = [n["midi"] for n in cf_response.json()["notes"]]
        
        # Generate counterpoint
        response = client.post("/api/generate-counterpoint", json={
            "tonic": 0,
            "mode": "ionian",
            "cf_notes": cf_notes,
            "cf_voice_range": "alto",
            "seed": 42
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "cf_notes" in data
        assert "cp_notes" in data
        assert "violations" in data
        assert len(data["cp_notes"]) == len(cf_notes)
    
    def test_generate_cf_invalid_length(self):
        """Test CF generation with invalid length."""
        response = client.post("/api/generate-cantus-firmus", json={
            "tonic": 0,
            "mode": "ionian",
            "length": 3,  # Too short
            "voice_range": "soprano"
        })
        
        assert response.status_code == 422
    
    def test_generate_cf_invalid_tonic(self):
        """Test CF generation with invalid tonic."""
        response = client.post("/api/generate-cantus-firmus", json={
            "tonic": 15,  # Out of range
            "mode": "ionian",
            "length": 8,
            "voice_range": "soprano"
        })
        
        assert response.status_code == 422
    
    def test_evaluate_counterpoint(self):
        """Test counterpoint evaluation endpoint."""
        response = client.post("/api/evaluate-counterpoint", json={
            "tonic": 0,
            "mode": "ionian",
            "cf_notes": [60, 62, 64, 65, 67, 69, 71, 72],
            "cp_notes": [67, 69, 71, 72, 74, 76, 77, 79]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "violations" in data
        assert "is_valid" in data
        assert isinstance(data["is_valid"], bool)
