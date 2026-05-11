from flask import Flask, render_template, request, Response, stream_with_context, send_file
import subprocess
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent.runner import AgentRunner

app = Flask(__name__, template_folder="templates")

agent = AgentRunner()

@app.route("/")
def index():
    """Serve the chat UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    SSE endpoint — streams agent response token by token.
    
    SSE format requires each message to be:
    data: <content>\n\n
    
    The browser's EventSource API reads this automatically.
    """
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return {"error": "Empty message"}, 400

    def generate():
        try:
            # Stream tokens from agent
            for chunk in agent.stream(user_input):
                data = json.dumps({"type": "token", "content": chunk})
                yield f"data: {data}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            error_msg = str(e)
            # If rate limited, tell user to wait
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                yield f"data: {json.dumps({'type': 'error', 'content': 'Rate limit hit — please wait 30 seconds and try again.'})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",           # tells browser this is SSE
        headers={
            "Cache-Control": "no-cache",        # don't cache streaming response
            "X-Accel-Buffering": "no"           # disable nginx buffering if deployed
        }
    )


@app.route("/clear", methods=["POST"])
def clear():
    """Clear conversation memory."""
    agent.clear_memory()
    return {"status": "cleared"}

@app.route("/benchmark")
def benchmark_dashboard():
    """Serve the benchmark dashboard image."""
    dashboard_path = "evaluation/results/dashboard.png"

    if not os.path.exists(dashboard_path):
        return {"error": "No benchmark results yet. Run evaluation/benchmark.py first."}, 404

    return send_file(dashboard_path, mimetype="image/png")


@app.route("/run-benchmark")
def run_benchmark_route():
    """Trigger benchmark run from browser."""
    try:
        subprocess.Popen(["python", "evaluation/benchmark.py"])
        return {"status": "Benchmark started. Check terminal for progress."}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
    