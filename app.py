from app import app, db

# Entry point - this is what runs when you start the Flask app
if __name__ == '__main__':
    # app_context is required to work with the database outside of requests
    with app.app_context():
        # Creates all tables defined in models.py if they dont exist yet
        # Safe to run multiple times - it wont overwrite existing tables
        db.create_all()
        print('Database tables created successfully')

    # debug=True means Flask auto reloads when you save changes
    # and shows detailed error pages - NEVER use debug=True in production
    app.run(debug=True)
