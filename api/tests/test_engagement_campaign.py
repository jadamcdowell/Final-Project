from fastapi.testclient import TestClient
from unittest import mock
from ..main import app  # Import your FastAPI app
from ..schemas.engagement_campaign import EngagementCampaignCreate

client = TestClient(app)

# Example sample data
sample_campaign = {
    "title": "New Year Campaign",
    "description": "Campaign for the new year",
    "status": "active",
    "start_date": "2024-12-01T00:00:00",
    "end_date": "2024-12-31T23:59:59"
}

# Test for creating an engagement campaign
def test_create_campaign():
    # Mocking the controller's create_campaign function
    with mock.patch("api.controllers.engagement_campaign.create_campaign") as mock_create_campaign:
        mock_create_campaign.return_value = {
            "id": 1,
            "title": sample_campaign["title"],
            "description": sample_campaign["description"],
            "status": sample_campaign["status"],
            "start_date": sample_campaign["start_date"],
            "end_date": sample_campaign["end_date"],
            "created_at": "2024-12-01T00:00:00"
        }

        # Include staff_id in the request
        staff_id = 50  # Example staff ID, replace with the correct value
        response = client.post("/engagement-campaigns/?staff_id=" + str(staff_id), json=sample_campaign)

        # Print response in case of failure
        if response.status_code != 200:
            print(response.json())  # Log the error details

        # Assertions to verify that the response is correct
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_campaign["title"]
        assert data["description"] == sample_campaign["description"]
        assert data["status"] == sample_campaign["status"]
        assert data["start_date"] == sample_campaign["start_date"]
        assert data["end_date"] == sample_campaign["end_date"]

def test_read_all_campaigns():
    # Mocking the controller's read_all_campaigns function
    with mock.patch("api.controllers.engagement_campaign.read_all_campaigns") as mock_read_all_campaigns:
        mock_read_all_campaigns.return_value = [{
            "id": 1,
            "title": sample_campaign["title"],
            "description": sample_campaign["description"],
            "status": sample_campaign["status"],
            "start_date": sample_campaign["start_date"],
            "end_date": sample_campaign["end_date"],
            "created_at": "2024-12-01T00:00:00"
        }]
        
        staff_id = 50  # Example staff ID, replace with the correct value
        response = client.get(f"/engagement-campaigns/?staff_id={staff_id}")

        # Assertions to verify that the response is correct
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1  # We are expecting one campaign in the mock data
        assert data[0]["title"] == sample_campaign["title"]

# Test for updating an engagement campaign
def test_update_campaign():
    # Mocking the controller's update_campaign function
    with mock.patch("api.controllers.engagement_campaign.update_campaign") as mock_update_campaign:
        mock_update_campaign.return_value = {
            "id": 1,
            "title": sample_campaign["title"],
            "description": sample_campaign["description"],
            "status": "updated",  # Simulating an updated status
            "start_date": sample_campaign["start_date"],
            "end_date": sample_campaign["end_date"],
            "created_at": "2024-12-01T00:00:00"
        }

        staff_id = 50  # Example staff ID
        campaign_id = 1  # Example campaign ID to update
        updated_campaign = {**sample_campaign, "status": "updated"}  # Modify the status to be updated
        response = client.put(f"/engagement-campaigns/{campaign_id}?staff_id={staff_id}", json=updated_campaign)

        # Assertions to verify that the response is correct
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "updated"

# Test for deleting an engagement campaign
def test_delete_campaign():
    # Mocking the controller's delete_campaign function
    with mock.patch("api.controllers.engagement_campaign.delete_campaign") as mock_delete_campaign:
        mock_delete_campaign.return_value = {"detail": "Campaign deleted successfully"}

        staff_id = 50  # Example staff ID
        campaign_id = 1  # Example campaign ID to delete
        response = client.delete(f"/engagement-campaigns/{campaign_id}?staff_id={staff_id}")

        # Assertions to verify that the response is correct
        assert response.status_code == 200
        data = response.json()
        assert data["detail"] == "Campaign deleted successfully"