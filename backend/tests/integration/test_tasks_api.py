"""Comprehensive API tests for Task CRUD endpoints.

This module contains 50+ tests covering:
- Authentication (missing, invalid, expired tokens)
- List tasks (empty, with tasks, statistics)
- Create task (valid, validation errors)
- Get task (success, not found, forbidden)
- Update task (full, partial, validation)
- Delete task (success, not found, forbidden)
- Toggle completion (success, idempotency)
- Multi-user isolation
- Edge cases and error scenarios

Test coverage target: 80%+ for Phase II capstone.
"""

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient


# =============================================================================
# Authentication Tests
# =============================================================================


class TestAuthentication:
    """Tests for authentication and authorization."""

    def test_list_tasks_without_auth_returns_422(self, client: TestClient):
        """Request without Authorization header returns 422."""
        response = client.get("/api/tasks/")
        assert response.status_code == 422

    def test_list_tasks_with_invalid_token_format_returns_401(self, client: TestClient):
        """Request with non-Bearer token format returns 401."""
        response = client.get(
            "/api/tasks/",
            headers={"Authorization": "InvalidFormat token123"}
        )
        assert response.status_code == 401
        assert "credentials" in response.json()["detail"].lower()

    def test_list_tasks_with_invalid_jwt_returns_401(self, client: TestClient):
        """Request with invalid JWT returns 401."""
        response = client.get(
            "/api/tasks/",
            headers={"Authorization": "Bearer invalid.jwt.token"}
        )
        assert response.status_code == 401

    def test_list_tasks_with_expired_token_returns_401(
        self, client: TestClient, expired_auth_headers: dict
    ):
        """Request with expired token returns 401."""
        response = client.get("/api/tasks/", headers=expired_auth_headers)
        assert response.status_code == 401

    def test_create_task_without_auth_returns_422(self, client: TestClient):
        """Create task without auth returns 422."""
        response = client.post("/api/tasks/", json={"title": "Test"})
        assert response.status_code == 422

    def test_get_task_without_auth_returns_422(self, client: TestClient):
        """Get task without auth returns 422."""
        response = client.get(f"/api/tasks/{uuid4()}")
        assert response.status_code == 422

    def test_update_task_without_auth_returns_422(self, client: TestClient):
        """Update task without auth returns 422."""
        response = client.put(f"/api/tasks/{uuid4()}", json={"title": "Test"})
        assert response.status_code == 422

    def test_delete_task_without_auth_returns_422(self, client: TestClient):
        """Delete task without auth returns 422."""
        response = client.delete(f"/api/tasks/{uuid4()}")
        assert response.status_code == 422

    def test_toggle_complete_without_auth_returns_422(self, client: TestClient):
        """Toggle complete without auth returns 422."""
        response = client.patch(f"/api/tasks/{uuid4()}/complete")
        assert response.status_code == 422


# =============================================================================
# List Tasks Tests
# =============================================================================


class TestListTasks:
    """Tests for GET /api/tasks/ endpoint."""

    def test_list_tasks_empty_returns_empty_list(
        self, client: TestClient, auth_headers: dict
    ):
        """New user has empty task list."""
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0
        assert data["completed"] == 0

    def test_list_tasks_returns_user_tasks(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Returns tasks for authenticated user."""
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["id"] == sample_task["id"]
        assert data["total"] == 1

    def test_list_tasks_returns_correct_statistics(
        self, client: TestClient, auth_headers: dict, multiple_tasks: list
    ):
        """Returns correct total and completed counts."""
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert data["completed"] == 2  # Two tasks marked complete in fixture

    def test_list_tasks_ordered_by_created_at_desc(
        self, client: TestClient, auth_headers: dict
    ):
        """Tasks are ordered by creation date, newest first."""
        # Create tasks
        for i in range(3):
            client.post(
                "/api/tasks/",
                json={"title": f"Task {i}"},
                headers=auth_headers
            )

        response = client.get("/api/tasks/", headers=auth_headers)
        tasks = response.json()["tasks"]

        # Verify order (newest first)
        for i in range(len(tasks) - 1):
            assert tasks[i]["created_at"] >= tasks[i + 1]["created_at"]

    def test_list_tasks_isolation_between_users(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """Each user only sees their own tasks."""
        # User 1 creates task
        client.post(
            "/api/tasks/",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )

        # User 2 creates task
        client.post(
            "/api/tasks/",
            json={"title": "User 2 Task"},
            headers=other_auth_headers
        )

        # User 1 only sees their task
        response1 = client.get("/api/tasks/", headers=auth_headers)
        assert len(response1.json()["tasks"]) == 1
        assert response1.json()["tasks"][0]["title"] == "User 1 Task"

        # User 2 only sees their task
        response2 = client.get("/api/tasks/", headers=other_auth_headers)
        assert len(response2.json()["tasks"]) == 1
        assert response2.json()["tasks"][0]["title"] == "User 2 Task"


# =============================================================================
# Create Task Tests
# =============================================================================


class TestCreateTask:
    """Tests for POST /api/tasks/ endpoint."""

    def test_create_task_with_valid_data_returns_201(
        self, client: TestClient, auth_headers: dict
    ):
        """Valid task creation returns 201 with task data."""
        response = client.post(
            "/api/tasks/",
            json={"title": "New Task", "description": "Task description"},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["is_complete"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_with_title_only_returns_201(
        self, client: TestClient, auth_headers: dict
    ):
        """Task creation with only title (no description) succeeds."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Title Only Task"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["description"] == ""

    def test_create_task_with_empty_title_returns_400(
        self, client: TestClient, auth_headers: dict
    ):
        """Empty title returns 400 Bad Request."""
        response = client.post(
            "/api/tasks/",
            json={"title": ""},
            headers=auth_headers
        )
        assert response.status_code == 400 or response.status_code == 422

    def test_create_task_with_whitespace_title_returns_400(
        self, client: TestClient, auth_headers: dict
    ):
        """Whitespace-only title returns 400 Bad Request."""
        response = client.post(
            "/api/tasks/",
            json={"title": "   "},
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_create_task_with_long_title_returns_400(
        self, client: TestClient, auth_headers: dict
    ):
        """Title exceeding 200 characters returns 400."""
        long_title = "x" * 201
        response = client.post(
            "/api/tasks/",
            json={"title": long_title},
            headers=auth_headers
        )
        assert response.status_code == 400 or response.status_code == 422

    def test_create_task_with_max_length_title_succeeds(
        self, client: TestClient, auth_headers: dict
    ):
        """Title at exactly 200 characters succeeds."""
        max_title = "x" * 200
        response = client.post(
            "/api/tasks/",
            json={"title": max_title},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["title"] == max_title

    def test_create_task_strips_whitespace_from_title(
        self, client: TestClient, auth_headers: dict
    ):
        """Title is trimmed of leading/trailing whitespace."""
        response = client.post(
            "/api/tasks/",
            json={"title": "  Trimmed Title  "},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Trimmed Title"

    def test_create_task_with_unicode_title_succeeds(
        self, client: TestClient, auth_headers: dict
    ):
        """Unicode characters in title are handled correctly."""
        response = client.post(
            "/api/tasks/",
            json={"title": "日本語タスク 🎉"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["title"] == "日本語タスク 🎉"

    def test_create_task_assigns_correct_user_id(
        self, client: TestClient, auth_headers: dict, user_id: str
    ):
        """Created task has correct user_id."""
        response = client.post(
            "/api/tasks/",
            json={"title": "User Task"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["user_id"] == user_id

    def test_create_task_without_title_returns_422(
        self, client: TestClient, auth_headers: dict
    ):
        """Missing title field returns 422 validation error."""
        response = client.post(
            "/api/tasks/",
            json={"description": "No title"},
            headers=auth_headers
        )
        assert response.status_code == 422


# =============================================================================
# Get Task Tests
# =============================================================================


class TestGetTask:
    """Tests for GET /api/tasks/{task_id} endpoint."""

    def test_get_task_returns_task(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Get task returns correct task data."""
        response = client.get(
            f"/api/tasks/{sample_task['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task["id"]
        assert data["title"] == sample_task["title"]

    def test_get_task_not_found_returns_404(
        self, client: TestClient, auth_headers: dict
    ):
        """Non-existent task returns 404."""
        response = client.get(
            f"/api/tasks/{uuid4()}",
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_task_owned_by_other_user_returns_403(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """Accessing another user's task returns 403."""
        # Create task as user 1
        create_response = client.post(
            "/api/tasks/",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Try to access as user 2
        response = client.get(
            f"/api/tasks/{task_id}",
            headers=other_auth_headers
        )
        assert response.status_code == 403
        assert "permission" in response.json()["detail"].lower()

    def test_get_task_with_invalid_uuid_returns_422(
        self, client: TestClient, auth_headers: dict
    ):
        """Invalid UUID format returns 422."""
        response = client.get(
            "/api/tasks/not-a-uuid",
            headers=auth_headers
        )
        assert response.status_code == 422


# =============================================================================
# Update Task Tests
# =============================================================================


class TestUpdateTask:
    """Tests for PUT /api/tasks/{task_id} endpoint."""

    def test_update_task_full_update_succeeds(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Full update of all fields succeeds."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={
                "title": "Updated Title",
                "description": "Updated description",
                "is_complete": True
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["is_complete"] is True

    def test_update_task_partial_update_title_only(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Partial update of title only preserves other fields."""
        original_desc = sample_task["description"]
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": "New Title"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["description"] == original_desc

    def test_update_task_updates_updated_at_timestamp(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Update modifies updated_at timestamp."""
        original_updated_at = sample_task["updated_at"]

        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": "Timestamp Test"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["updated_at"] != original_updated_at

    def test_update_task_not_found_returns_404(
        self, client: TestClient, auth_headers: dict
    ):
        """Update non-existent task returns 404."""
        response = client.put(
            f"/api/tasks/{uuid4()}",
            json={"title": "Updated"},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_task_owned_by_other_user_returns_403(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """Updating another user's task returns 403."""
        # Create task as user 1
        create_response = client.post(
            "/api/tasks/",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Try to update as user 2
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hijacked"},
            headers=other_auth_headers
        )
        assert response.status_code == 403

    def test_update_task_with_empty_title_returns_400(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Update with empty title returns 400."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": ""},
            headers=auth_headers
        )
        assert response.status_code == 400 or response.status_code == 422

    def test_update_task_with_long_title_returns_400(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Update with title > 200 chars returns 400."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": "x" * 201},
            headers=auth_headers
        )
        assert response.status_code == 400 or response.status_code == 422


# =============================================================================
# Delete Task Tests
# =============================================================================


class TestDeleteTask:
    """Tests for DELETE /api/tasks/{task_id} endpoint."""

    def test_delete_task_returns_204(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Successful delete returns 204 No Content."""
        response = client.delete(
            f"/api/tasks/{sample_task['id']}",
            headers=auth_headers
        )
        assert response.status_code == 204
        assert response.content == b""

    def test_delete_task_removes_task(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Deleted task is no longer accessible."""
        # Delete
        client.delete(f"/api/tasks/{sample_task['id']}", headers=auth_headers)

        # Try to get
        response = client.get(
            f"/api/tasks/{sample_task['id']}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_task_not_found_returns_404(
        self, client: TestClient, auth_headers: dict
    ):
        """Delete non-existent task returns 404."""
        response = client.delete(
            f"/api/tasks/{uuid4()}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_task_owned_by_other_user_returns_403(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """Deleting another user's task returns 403."""
        # Create task as user 1
        create_response = client.post(
            "/api/tasks/",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Try to delete as user 2
        response = client.delete(
            f"/api/tasks/{task_id}",
            headers=other_auth_headers
        )
        assert response.status_code == 403

    def test_delete_task_idempotent_returns_404_on_second_call(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Second delete of same task returns 404."""
        # First delete
        client.delete(f"/api/tasks/{sample_task['id']}", headers=auth_headers)

        # Second delete
        response = client.delete(
            f"/api/tasks/{sample_task['id']}",
            headers=auth_headers
        )
        assert response.status_code == 404


# =============================================================================
# Toggle Completion Tests
# =============================================================================


class TestToggleCompletion:
    """Tests for PATCH /api/tasks/{task_id}/complete endpoint."""

    def test_toggle_complete_from_false_to_true(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Toggle incomplete task to complete."""
        assert sample_task["is_complete"] is False

        response = client.patch(
            f"/api/tasks/{sample_task['id']}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["is_complete"] is True

    def test_toggle_complete_from_true_to_false(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Toggle complete task back to incomplete."""
        # First toggle to complete
        client.patch(
            f"/api/tasks/{sample_task['id']}/complete",
            headers=auth_headers
        )

        # Second toggle back to incomplete
        response = client.patch(
            f"/api/tasks/{sample_task['id']}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["is_complete"] is False

    def test_toggle_complete_updates_timestamp(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Toggle updates updated_at timestamp."""
        original_updated_at = sample_task["updated_at"]

        response = client.patch(
            f"/api/tasks/{sample_task['id']}/complete",
            headers=auth_headers
        )
        assert response.json()["updated_at"] != original_updated_at

    def test_toggle_complete_not_found_returns_404(
        self, client: TestClient, auth_headers: dict
    ):
        """Toggle non-existent task returns 404."""
        response = client.patch(
            f"/api/tasks/{uuid4()}/complete",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_toggle_complete_owned_by_other_user_returns_403(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """Toggling another user's task returns 403."""
        # Create task as user 1
        create_response = client.post(
            "/api/tasks/",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Try to toggle as user 2
        response = client.patch(
            f"/api/tasks/{task_id}/complete",
            headers=other_auth_headers
        )
        assert response.status_code == 403


# =============================================================================
# Multi-User Isolation Tests
# =============================================================================


class TestMultiUserIsolation:
    """Tests for user data isolation."""

    def test_user_cannot_see_other_user_tasks_in_list(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """User's task list only contains their own tasks."""
        # Create tasks for both users
        client.post(
            "/api/tasks/",
            json={"title": "User 1 Task A"},
            headers=auth_headers
        )
        client.post(
            "/api/tasks/",
            json={"title": "User 1 Task B"},
            headers=auth_headers
        )
        client.post(
            "/api/tasks/",
            json={"title": "User 2 Task"},
            headers=other_auth_headers
        )

        # User 1 sees only their 2 tasks
        response1 = client.get("/api/tasks/", headers=auth_headers)
        assert response1.json()["total"] == 2
        titles = [t["title"] for t in response1.json()["tasks"]]
        assert "User 2 Task" not in titles

        # User 2 sees only their 1 task
        response2 = client.get("/api/tasks/", headers=other_auth_headers)
        assert response2.json()["total"] == 1

    def test_user_task_operations_isolated(
        self, client: TestClient, auth_headers: dict, other_auth_headers: dict
    ):
        """All CRUD operations are isolated by user."""
        # User 1 creates task
        create_resp = client.post(
            "/api/tasks/",
            json={"title": "Private Task"},
            headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User 2 cannot get it
        get_resp = client.get(
            f"/api/tasks/{task_id}",
            headers=other_auth_headers
        )
        assert get_resp.status_code == 403

        # User 2 cannot update it
        update_resp = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hijacked"},
            headers=other_auth_headers
        )
        assert update_resp.status_code == 403

        # User 2 cannot toggle it
        toggle_resp = client.patch(
            f"/api/tasks/{task_id}/complete",
            headers=other_auth_headers
        )
        assert toggle_resp.status_code == 403

        # User 2 cannot delete it
        delete_resp = client.delete(
            f"/api/tasks/{task_id}",
            headers=other_auth_headers
        )
        assert delete_resp.status_code == 403


# =============================================================================
# Edge Cases and Error Scenarios
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and error scenarios."""

    def test_task_with_special_characters_in_title(
        self, client: TestClient, auth_headers: dict
    ):
        """Special characters are handled correctly."""
        special_title = "<script>alert('xss')</script> & \"quotes\" 'apostrophe'"
        response = client.post(
            "/api/tasks/",
            json={"title": special_title},
            headers=auth_headers
        )
        assert response.status_code == 201
        # Title should be stored as-is (XSS prevention is frontend concern)
        assert response.json()["title"] == special_title

    def test_task_with_newlines_in_description(
        self, client: TestClient, auth_headers: dict
    ):
        """Newlines in description are preserved."""
        desc_with_newlines = "Line 1\nLine 2\n\nLine 4"
        response = client.post(
            "/api/tasks/",
            json={"title": "Multiline", "description": desc_with_newlines},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["description"] == desc_with_newlines

    def test_empty_request_body_returns_422(
        self, client: TestClient, auth_headers: dict
    ):
        """Empty request body returns 422."""
        response = client.post(
            "/api/tasks/",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_null_description_treated_as_empty_string(
        self, client: TestClient, auth_headers: dict
    ):
        """Null description is stored as empty string."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Test", "description": None},
            headers=auth_headers
        )
        # Should either succeed with empty string or return validation error
        if response.status_code == 201:
            assert response.json()["description"] == ""

    def test_extra_fields_in_request_are_ignored(
        self, client: TestClient, auth_headers: dict
    ):
        """Extra fields in request body are ignored."""
        response = client.post(
            "/api/tasks/",
            json={
                "title": "Test",
                "extra_field": "should be ignored",
                "another_extra": 123
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert "extra_field" not in data
        assert "another_extra" not in data


# =============================================================================
# Health Check Tests
# =============================================================================


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check_returns_200(self, client: TestClient):
        """Health check returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_status_healthy(self, client: TestClient):
        """Health check response contains healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


# =============================================================================
# Validation Constants Tests
# =============================================================================


class TestValidationConstants:
    """Tests validating constants match between model and API."""

    def test_max_description_length_accepted(
        self, client: TestClient, auth_headers: dict
    ):
        """Description at max length (2000 chars) succeeds."""
        max_desc = "x" * 2000
        response = client.post(
            "/api/tasks/",
            json={"title": "Test", "description": max_desc},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert len(response.json()["description"]) == 2000

    def test_description_over_max_length_fails(
        self, client: TestClient, auth_headers: dict
    ):
        """Description over 2000 chars returns validation error."""
        long_desc = "x" * 2001
        response = client.post(
            "/api/tasks/",
            json={"title": "Test", "description": long_desc},
            headers=auth_headers
        )
        # Should return validation error
        assert response.status_code == 422


# =============================================================================
# v2.0.0 Fields Tests (Priority, Category, Due Date)
# =============================================================================


class TestTaskPriorityField:
    """Tests for v2.0.0 priority field."""

    def test_create_task_with_default_priority(
        self, client: TestClient, auth_headers: dict
    ):
        """Task created without priority gets 'medium' default."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Test Priority Default"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["priority"] == "medium"

    def test_create_task_with_high_priority(
        self, client: TestClient, auth_headers: dict
    ):
        """Task can be created with 'high' priority."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Urgent Task", "priority": "high"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["priority"] == "high"

    def test_create_task_with_low_priority(
        self, client: TestClient, auth_headers: dict
    ):
        """Task can be created with 'low' priority."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Low Priority Task", "priority": "low"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["priority"] == "low"

    def test_update_task_priority(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Task priority can be updated."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"priority": "high"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["priority"] == "high"

    def test_task_priority_in_read_response(
        self, client: TestClient, auth_headers: dict
    ):
        """Priority is included in task read response."""
        create_response = client.post(
            "/api/tasks/",
            json={"title": "Check Priority", "priority": "low"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        get_response = client.get(
            f"/api/tasks/{task_id}",
            headers=auth_headers
        )
        assert "priority" in get_response.json()
        assert get_response.json()["priority"] == "low"


class TestTaskCategoryField:
    """Tests for v2.0.0 category field."""

    def test_create_task_with_default_category(
        self, client: TestClient, auth_headers: dict
    ):
        """Task created without category gets 'general' default."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Test Category Default"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["category"] == "general"

    def test_create_task_with_work_category(
        self, client: TestClient, auth_headers: dict
    ):
        """Task can be created with 'work' category."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Work Task", "category": "work"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["category"] == "work"

    def test_create_task_with_custom_category(
        self, client: TestClient, auth_headers: dict
    ):
        """Task can be created with custom category."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Custom Category Task", "category": "fitness"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["category"] == "fitness"

    def test_update_task_category(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Task category can be updated."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"category": "personal"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["category"] == "personal"

    def test_category_max_length(
        self, client: TestClient, auth_headers: dict
    ):
        """Category at max length (50 chars) succeeds."""
        max_category = "x" * 50
        response = client.post(
            "/api/tasks/",
            json={"title": "Max Category", "category": max_category},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert len(response.json()["category"]) == 50


class TestTaskDueDateField:
    """Tests for v2.0.0 due_date field."""

    def test_create_task_with_no_due_date(
        self, client: TestClient, auth_headers: dict
    ):
        """Task created without due_date has null due_date."""
        response = client.post(
            "/api/tasks/",
            json={"title": "No Due Date Task"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["due_date"] is None

    def test_create_task_with_due_date(
        self, client: TestClient, auth_headers: dict
    ):
        """Task can be created with due_date."""
        response = client.post(
            "/api/tasks/",
            json={"title": "Task with Due Date", "due_date": "2025-12-25"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["due_date"] == "2025-12-25"

    def test_update_task_due_date(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Task due_date can be updated."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"due_date": "2025-12-31"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["due_date"] == "2025-12-31"

    def test_due_date_format_iso8601(
        self, client: TestClient, auth_headers: dict
    ):
        """Due date accepts ISO 8601 format (YYYY-MM-DD)."""
        response = client.post(
            "/api/tasks/",
            json={"title": "ISO Date Task", "due_date": "2025-06-15"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["due_date"] == "2025-06-15"

    def test_due_date_in_list_response(
        self, client: TestClient, auth_headers: dict
    ):
        """Due date is included in task list response."""
        client.post(
            "/api/tasks/",
            json={"title": "Due Date List Test", "due_date": "2025-01-15"},
            headers=auth_headers
        )

        response = client.get("/api/tasks/", headers=auth_headers)
        tasks = response.json()["tasks"]
        task = next(t for t in tasks if t["title"] == "Due Date List Test")
        assert task["due_date"] == "2025-01-15"


class TestV2FieldsCombination:
    """Tests for combining v2.0.0 fields (priority, category, due_date)."""

    def test_create_task_with_all_v2_fields(
        self, client: TestClient, auth_headers: dict
    ):
        """Task can be created with all v2.0.0 fields."""
        response = client.post(
            "/api/tasks/",
            json={
                "title": "Complete v2 Task",
                "description": "Has all v2.0.0 fields",
                "priority": "high",
                "category": "work",
                "due_date": "2025-12-20"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["priority"] == "high"
        assert data["category"] == "work"
        assert data["due_date"] == "2025-12-20"

    def test_update_multiple_v2_fields(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Multiple v2.0.0 fields can be updated together."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={
                "priority": "low",
                "category": "study",
                "due_date": "2025-11-30"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["priority"] == "low"
        assert data["category"] == "study"
        assert data["due_date"] == "2025-11-30"

    def test_v2_fields_in_task_list(
        self, client: TestClient, auth_headers: dict
    ):
        """All v2.0.0 fields appear in task list response."""
        client.post(
            "/api/tasks/",
            json={
                "title": "v2 Fields in List",
                "priority": "medium",
                "category": "shopping",
                "due_date": "2025-12-24"
            },
            headers=auth_headers
        )

        response = client.get("/api/tasks/", headers=auth_headers)
        tasks = response.json()["tasks"]
        task = next(t for t in tasks if t["title"] == "v2 Fields in List")
        assert "priority" in task
        assert "category" in task
        assert "due_date" in task

    def test_partial_v2_fields_update(
        self, client: TestClient, auth_headers: dict, sample_task: dict
    ):
        """Updating one v2 field preserves others."""
        # First set all v2 fields
        client.put(
            f"/api/tasks/{sample_task['id']}",
            json={
                "priority": "high",
                "category": "work",
                "due_date": "2025-12-25"
            },
            headers=auth_headers
        )

        # Update only priority
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"priority": "low"},
            headers=auth_headers
        )

        data = response.json()
        assert data["priority"] == "low"
        # Other v2 fields should be preserved
        assert data["category"] == "work"
        assert data["due_date"] == "2025-12-25"
