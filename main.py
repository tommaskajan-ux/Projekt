import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")

from minio import Minio
from minio.error import S3Error
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

db = SQLAlchemy()
migrate = Migrate()


def get_minio_client():
    return Minio(
        os.getenv("AWS_ENDPOINT_URL", "127.0.0.1:9000").replace("http://", "").replace("https://", ""),
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        secure=False
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
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

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
            client = get_minio_client()
            bucket = os.getenv("S3_BUCKET_NAME", "documents")

            if not client.bucket_exists(bucket):
                client.make_bucket(bucket)

            return jsonify(minio="ok", bucket=bucket)
        except S3Error as e:
            return jsonify(minio="error", error=str(e)), 500

    return app
