import json
import uuid
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.services import report_generator
from app import store

bp = Blueprint("report", __name__, url_prefix="/api/report")

REPORT_TYPES = [
    "CFO Monthly Board Report",
    "Quarterly Financial Review",
    "Annual Financial Summary",
    "Scenario Impact Report",
    "Cash Flow Analysis",
    "Budget vs Actuals Report",
    "Investor Update",
    "Custom Report",
]


@bp.route("/types", methods=["GET"])
def get_report_types():
    return jsonify(REPORT_TYPES)


@bp.route("/generate", methods=["POST"])
def generate_report():
    data = request.get_json()
    report_type = (data or {}).get("report_type", "CFO Monthly Board Report")
    instructions = (data or {}).get("instructions", "")

    report_id = str(uuid.uuid4())
    result_buffer = []

    def generate():
        try:
            for chunk in report_generator.stream_report(
                kpis=store["kpis"],
                scenarios=store["scenarios"],
                report_type=report_type,
                instructions=instructions,
            ):
                result_buffer.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"

            store["reports"].append({
                "id": report_id,
                "type": report_type,
                "content": "".join(result_buffer),
            })
            yield f"data: {json.dumps({'done': True, 'id': report_id})}\n\n"
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
        {"id": r["id"], "type": r["type"], "preview": r["content"][:200]}
        for r in store["reports"]
    ])


@bp.route("/<report_id>", methods=["GET"])
def get_report(report_id):
    for r in store["reports"]:
        if r["id"] == report_id:
            return jsonify(r)
    return jsonify({"error": "Not found"}), 404


@bp.route("/<report_id>", methods=["DELETE"])
def delete_report(report_id):
    store["reports"] = [r for r in store["reports"] if r["id"] != report_id]
    return jsonify({"message": "Deleted"})
