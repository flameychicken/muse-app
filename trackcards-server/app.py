from flask import Flask, send_from_directory, request, redirect
import os

app = Flask(__name__, static_folder="public", static_url_path="")

# Serve the AASA file as before
@app.route("/.well-known/apple-app-site-association")
def aasa():
    dirpath = os.path.join(app.static_folder, ".well-known")
    return send_from_directory(
        directory=dirpath,
        path="apple-app-site-association",
        mimetype="application/json"
    )

# OAuth callback endpoint
@app.route("/spotify/callback")
def spotify_callback():
    code  = request.args.get("code")
    error = request.args.get("error")
    if error:
        return f"❌ Spotify error: {error}"
    if not code:
        return "❌ Sorry no code in callback URL"
    # **Redirect immediately** into your app via custom scheme
    return redirect(f"trackcards://callback?code={code}", code=302)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
