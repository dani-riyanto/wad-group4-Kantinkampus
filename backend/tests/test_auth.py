import os
import unittest

os.environ["DATABASE_URL"] = "sqlite://"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import database, models
from app.main import app


class AuthorizationWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        models.Base.metadata.create_all(bind=cls.engine)
        cls.session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.engine
        )
        cls.original_session_local = database.SessionLocal
        database.SessionLocal = cls.session_factory
        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client_context.__exit__(None, None, None)
        database.SessionLocal = cls.original_session_local
        cls.engine.dispose()

    def login(self, username):
        response = self.client.post(
            "/auth/login", json={"username": username, "password": "12345"}
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertNotIn("access_token", response.json())
        self.assertNotIn("csrf_token", response.json())
        self.assertIn("HttpOnly", response.headers["set-cookie"])
        return self.client.cookies.get("csrf_token")

    def test_authentication_and_role_ownership_are_enforced(self):
        self.assertEqual(self.client.get("/sessions").status_code, 401)
        self.assertEqual(self.client.get("/menus").status_code, 401)

        admin_csrf = self.login("admin")
        created_users = {}
        self.assertEqual(self.client.get("/users").status_code, 200)

        for username in ("userA", "userB", "userC"):
            response = self.client.post(
                "/users",
                headers={"X-CSRF-Token": admin_csrf},
                json={"username": username, "password": "12345"},
            )
            self.assertEqual(response.status_code, 201, response.text)
            self.assertEqual(response.json()["role"], "user")
            created_users[username] = response.json()

        menu_response = self.client.post(
            "/menus",
            headers={"X-CSRF-Token": admin_csrf},
            json={
                "nama": "Nasi Uji",
                "harga": 12000,
                "kategori": "Makanan",
                "tersedia": True,
            },
        )
        self.assertEqual(menu_response.status_code, 201, menu_response.text)
        menu_id = menu_response.json()["id"]

        user_a_csrf = self.login("userA")
        self.assertEqual(self.client.get("/auth/session").status_code, 200)
        self.assertEqual(self.client.post("/users", json={"username": "userD", "password": "12345"}).status_code, 403)
        self.assertEqual(
            self.client.post(
                "/menus",
                headers={"X-CSRF-Token": user_a_csrf},
                json={
                    "nama": "Menu Terlarang",
                    "harga": 1000,
                    "kategori": "Makanan",
                    "tersedia": True,
                },
            ).status_code,
            403,
        )

        create_order = self.client.post(
            "/sessions",
            headers={"X-CSRF-Token": user_a_csrf},
            json={
                "customer_name": "User A",
                "menu_item_id": menu_id,
                "quantity": 2,
                "notes": "Catatan",
            },
        )
        self.assertEqual(create_order.status_code, 201, create_order.text)
        order = create_order.json()
        self.assertEqual(order["owner_id"], created_users["userA"]["id"])
        self.assertEqual(order["status"], "Baru")
        self.assertEqual(order["total_price"], 24000)

        response = self.client.patch(
            f"/users/{created_users['userA']['id']}",
            headers={"X-CSRF-Token": user_a_csrf},
            json={"display_name": "User A updated"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["display_name"], "User A updated")

        response = self.client.patch(f"/sessions/{order['id']}", json={"notes": "CSRF hilang"})
        self.assertEqual(response.status_code, 403)
        response = self.client.patch(
            f"/sessions/{order['id']}",
            headers={"X-CSRF-Token": user_a_csrf},
            json={"status": "Selesai"},
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.patch(
            f"/sessions/{order['id']}",
            headers={"X-CSRF-Token": user_a_csrf},
            json={"notes": "Catatan diperbarui"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["notes"], "Catatan diperbarui")

        self.client.delete("/auth/logout", headers={"X-CSRF-Token": user_a_csrf})
        self.assertEqual(
            self.client.get("/users/me").status_code,
            401,
        )

        user_b_csrf = self.login("userB")
        self.assertEqual(self.client.get("/sessions").json(), [])
        self.assertEqual(self.client.get("/users").status_code, 403)
        self.assertEqual(
            self.client.delete(
                f"/users/{created_users['userA']['id']}",
                headers={"X-CSRF-Token": user_b_csrf},
            ).status_code,
            403,
        )
        response = self.client.patch(
            f"/users/{created_users['userA']['id']}",
            headers={"X-CSRF-Token": user_b_csrf},
            json={"display_name": "Unauthorized change"},
        )
        self.assertEqual(response.status_code, 403, response.text)

        response = self.client.patch(
            f"/sessions/{order['id']}",
            headers={"X-CSRF-Token": user_b_csrf},
            json={"notes": "Unauthorized change"},
        )
        self.assertEqual(response.status_code, 404, response.text)

        response = self.client.delete(
            f"/sessions/{order['id']}",
            headers={"X-CSRF-Token": user_b_csrf},
        )
        self.assertEqual(response.status_code, 404, response.text)

        user_a_csrf = self.login("userA")
        response = self.client.get(
            f"/sessions/{order['id']}"
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["notes"], "Catatan diperbarui")

        self.client.delete("/auth/logout", headers={"X-CSRF-Token": user_a_csrf})
        admin_csrf = self.login("admin")
        admin_orders = self.client.get("/sessions").json()
        self.assertEqual(len(admin_orders), 1)
        admin_users = self.client.get("/users").json()
        self.assertEqual(
            {user["username"] for user in admin_users},
            {"userA", "userB", "userC"},
        )
        self.assertEqual(
            self.client.delete(
                f"/users/{created_users['userA']['id']}",
                headers={"X-CSRF-Token": admin_csrf},
            ).status_code,
            204,
        )
        db = self.session_factory()
        saved_order = db.query(models.Order).filter(models.Order.id == order["id"]).one()
        admin = db.query(models.User).filter(models.User.username == "admin").one()
        self.assertEqual(saved_order.owner_id, admin.id)
        self.assertIsNone(
            db.query(models.User).filter(models.User.username == "userA").first()
        )
        db.close()
        self.assertEqual(
            self.client.post(
                "/auth/login",
                json={"username": "userA", "password": "12345"},
            ).status_code,
            401,
        )
        self.assertEqual(
            self.client.delete(
                f"/users/{admin.id}",
                headers={"X-CSRF-Token": admin_csrf},
            ).status_code,
            409,
        )
        response = self.client.patch(
            f"/sessions/{order['id']}",
            headers={"X-CSRF-Token": admin_csrf},
            json={"status": "Diproses"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "Diproses")


if __name__ == "__main__":
    unittest.main()
