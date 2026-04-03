import json
import uuid
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.services import scenario_engine
from app import store

bp = Blueprint("scenario", __name__, url_prefix="/api/scenario")


@bp.route("/run", methods=["POST"])
def run_scenario():
    data = request.get_json()
    scenario_desc = (data or {}).get("scenario", "").strip()
    if not scenario_desc:
        return jsonify({"error": "Scenario description is required"}), 400

    # Build context from uploaded documents
    context_parts = []
    for doc in store["documents"]:
        context_parts.append(f"### Document: {doc['filename']}\n{doc['text'][:10000]}")
    context = "\n\n".join(context_parts)

    scenario_id = str(uuid.uuid4())
    result_buffer = []

    def generate():
        try:
            for chunk in scenario_engine.stream_scenario(context, scenario_desc):
                result_buffer.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            # Persist the result
            store["scenarios"].append({
                "id": scenario_id,
                "scenario": scenario_desc,
                "result": "".join(result_buffer),
            })
            yield f"data: {json.dumps({'done': True, 'id': scenario_id})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )


@bp.route("/history", methods=["GET"])
def get_history():
    return jsonify([
        {"id": s["id"], "scenario": s["scenario"], "preview": s["result"][:200]}
        for s in store["scenarios"]
    ])


@bp.route("/<scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    for s in store["scenarios"]:
        if s["id"] == scenario_id:
            return jsonify(s)
    return jsonify({"error": "Not found"}), 404


@bp.route("/<scenario_id>", methods=["DELETE"])
def delete_scenario(scenario_id):
    store["scenarios"] = [s for s in store["scenarios"] if s["id"] != scenario_id]
    return jsonify({"message": "Deleted"})
