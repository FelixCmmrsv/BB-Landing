from quart import Blueprint, request, jsonify, render_template
import backend.app.database.requests as rq
from backend.app.handlers import notify_new_user

registration = Blueprint("registration", __name__)

@registration.route("/", methods=["GET"])
async def registration_form():
    return await render_template("register.html")

@registration.route("/submit", methods=["POST"])
async def submit_form():
    try:
        data = await request.form
        first_name = data.get("first-name")
        last_name = data.get("last-name")
        username = data.get("username")
        email = data.get("email")
        profile = data.get("profile-link")
        description = data.get("comments")
        agree = data.get("agree")

        print(f"Data received: {data}")

        if not all([first_name, last_name, username, email]) or agree != 'on':
            return jsonify({"status": "error", "message": "All required fields must be filled."}), 400

        await rq.add_user(
            first_name,
            last_name,
            username,
            email,
            profile,
            description
        )

        new_user = await rq.get_user_by_username(username)
        if new_user:
            await notify_new_user(new_user)

        return jsonify({"status": "success", "message": "User registered successfully!"})
    except Exception as e:
        print(f"Error during form submission: {e}")
        return jsonify({"status": "error", "message": "An error occurred while processing the request."}), 500
