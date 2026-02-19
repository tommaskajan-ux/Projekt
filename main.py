import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")

import boto3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

db = SQLAlchemy()
migrate = Migrate()


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        region_name=os.getenv("S3_REGION", "us-east-1"),
    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_name = db.Column(db.String(512), nullable=False)
    minio_key = db.Column(db.String(1024), unique=True, nullable=False)
    size_bytes = db.Column(db.BigInteger, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)  # THIS must be inside create_app

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/db-check")
    def db_check():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(db="ok")
        except Exception as e:
            return jsonify(db="error", error=str(e)), 500

    @app.get("/minio-check")
    def minio_check():
        try:
            s3 = s3_client()
            bucket = os.getenv("S3_BUCKET", "uploads")
            existing = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
            if bucket not in existing:
                s3.create_bucket(Bucket=bucket)
            return jsonify(minio="ok", bucket=bucket)
        except Exception as e:
            return jsonify(minio="error", error=str(e)), 500

    return app
