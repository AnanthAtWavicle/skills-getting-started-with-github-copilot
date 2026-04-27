"""
Unit tests for the Mergington High School Activities API.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities."""
        # Arrange
        # No setup needed - using default fixture state
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball Team" in data

    def test_get_activities_returns_activity_details(self, client):
        """Test that activity details are returned correctly."""
        # Arrange
        # No setup needed - using default fixture state
        
        # Act
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        # Assert
        assert response.status_code == 200
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_returns_participants(self, client):
        """Test that participants list is included in activity details."""
        # Arrange
        # No setup needed - using default fixture state
        
        # Act
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        # Assert
        assert response.status_code == 200
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Basketball Team"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in data["message"]
        assert email in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup adds the participant to the activity."""
        # Arrange
        email = "test@mergington.edu"
        activity = "Soccer Club"
        
        # Act
        client.post(f"/activities/{activity}/signup?email={email}")
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert email in data[activity]["participants"]

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns 404."""
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_participant_returns_400(self, client):
        """Test that duplicate signup returns 400 error."""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        # Email is already registered in default fixture state
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_multiple_students_different_activities(self, client):
        """Test that multiple students can signup for different activities."""
        # Arrange
        student1_email = "student1@mergington.edu"
        student2_email = "student2@mergington.edu"
        activity1 = "Basketball Team"
        activity2 = "Soccer Club"
        
        # Act
        client.post(f"/activities/{activity1}/signup?email={student1_email}")
        client.post(f"/activities/{activity2}/signup?email={student2_email}")
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert student1_email in data[activity1]["participants"]
        assert student2_email in data[activity2]["participants"]

    def test_signup_multiple_students_same_activity(self, client):
        """Test that multiple students can signup for the same activity."""
        # Arrange
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        activity = "Art Club"
        
        # Act
        for email in emails:
            client.post(f"/activities/{activity}/signup?email={email}")
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data[activity]["participants"]) == 3
        for email in emails:
            assert email in data[activity]["participants"]


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity."""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        # Email is already registered in default fixture state
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister removes the participant from the activity."""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        # Email is already registered in default fixture state
        
        # Act
        client.delete(f"/activities/{activity}/signup?email={email}")
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert email not in data[activity]["participants"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregister from non-existent activity returns 404."""
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_nonexistent_participant_returns_400(self, client):
        """Test that unregistering non-signed-up student returns 400."""
        # Arrange
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"

    def test_unregister_allows_re_signup(self, client):
        """Test that after unregistering, a student can sign up again."""
        # Arrange
        email = "student@mergington.edu"
        activity = "Basketball Team"
        
        # Act - First signup
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act - Unregister
        client.delete(f"/activities/{activity}/signup?email={email}")
        
        # Act - Re-signup
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200

    def test_unregister_preserves_other_participants(self, client):
        """Test that unregistering one student doesn't affect others."""
        # Arrange
        email_to_remove = "john@mergington.edu"
        email_to_preserve = "olivia@mergington.edu"
        activity = "Gym Class"
        # Both emails are already registered in default fixture state
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email_to_remove}"
        )
        activities_response = client.get("/activities")
        data = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert email_to_remove not in data[activity]["participants"]
        assert email_to_preserve in data[activity]["participants"]


class TestActivityCapacity:
    """Tests for activity capacity limits."""

    def test_availability_badge_calculation(self, client):
        """Test that available spots are calculated correctly."""
        # Arrange
        # No setup needed - using default fixture state
        
        # Act
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        prog_class = data["Programming Class"]
        
        chess_club_spots_left = chess_club["max_participants"] - len(chess_club["participants"])
        prog_class_spots_left = prog_class["max_participants"] - len(prog_class["participants"])
        
        # Assert
        # Chess Club: 12 max, 2 participants = 10 spots left
        assert chess_club_spots_left == 10
        # Programming Class: 20 max, 2 participants = 18 spots left
        assert prog_class_spots_left == 18


class TestActivityCardIntegration:
    """Integration tests for activity card functionality."""

    def test_signup_and_unregister_workflow(self, client):
        """Test the complete signup and unregister workflow."""
        # Arrange
        email = "integration@mergington.edu"
        activity = "Drama Club"
        
        # Act - Sign up
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert signup success
        assert signup_response.status_code == 200
        
        # Act - Verify participant is added
        response = client.get("/activities")
        data = response.json()
        
        # Assert participant added
        assert email in data[activity]["participants"]
        
        # Act - Unregister
        unregister_response = client.delete(f"/activities/{activity}/signup?email={email}")
        
        # Assert unregister success
        assert unregister_response.status_code == 200
        
        # Act - Verify participant is removed
        response = client.get("/activities")
        data = response.json()
        
        # Assert participant removed
        assert email not in data[activity]["participants"]

    def test_multiple_operations_maintain_state(self, client):
        """Test that multiple operations maintain correct state."""
        # Arrange
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        activity = "Science Club"
        email_to_remove = "student2@mergington.edu"
        
        # Act - Add three students
        for email in emails:
            client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act - Remove middle student
        client.delete(f"/activities/{activity}/signup?email={email_to_remove}")
        
        # Act - Verify state
        response = client.get("/activities")
        data = response.json()
        participants = data[activity]["participants"]
        
        # Assert
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" not in participants
        assert "student3@mergington.edu" in participants
        assert len(participants) == 2
