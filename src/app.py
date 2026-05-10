from flask import Flask, render_template, request, Response, stream_with_context
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent.runner import AgentRunner

app = Flask(__name__, template_folder="../templates")

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
                # SSE format — must be exactly this format
                data = json.dumps({"type": "token", "content": chunk})
                yield f"data: {data}\n\n"

            # Signal to browser that streaming is done
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            error_data = json.dumps({"type": "error", "content": str(e)})
            yield f"data: {error_data}\n\n"

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


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
    