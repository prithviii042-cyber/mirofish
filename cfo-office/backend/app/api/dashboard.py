import json
from flask import Blueprint, request, jsonify
from app.services import document_processor, kpi_extractor
from app import store

bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@bp.route("/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    file_bytes = file.read()
    if len(file_bytes) > 20 * 1024 * 1024:
        return jsonify({"error": "File exceeds 20 MB limit"}), 413

    text = document_processor.extract_text(file.filename, file_bytes)
    if not text.strip():
        return jsonify({"error": "Could not extract text from file"}), 422

    result = kpi_extractor.extract_kpis(text)

    doc_entry = {
        "filename": file.filename,
        "text": text[:50000],
        "kpis": result.get("kpis", []),
        "summary": result.get("summary", ""),
        "period": result.get("period"),
        "company": result.get("company"),
    }
    store["documents"].append(doc_entry)
    store["kpis"].extend(result.get("kpis", []))

    return jsonify({
        "filename": file.filename,
        "kpi_count": len(result.get("kpis", [])),
        "summary": result.get("summary", ""),
        "period": result.get("period"),
        "company": result.get("company"),
        "kpis": result.get("kpis", []),
    })


@bp.route("/kpis", methods=["GET"])
def get_kpis():
    return jsonify({"kpis": store["kpis"], "documents": [
        {"filename": d["filename"], "period": d.get("period"), "company": d.get("company")}
        for d in store["documents"]
    ]})


@bp.route("/kpis", methods=["DELETE"])
def clear_kpis():
    store["kpis"].clear()
    store["documents"].clear()
    return jsonify({"message": "Cleared"})
