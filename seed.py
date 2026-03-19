from app import app, db
from app.models import Faculty, Subject

with app.app_context():
    fai = Faculty.query.filter_by(code="FAI").first()

    if not fai:
        fai = Faculty(
            name="Faculty of Applied Informatics",
            code="FAI"
        )
        db.session.add(fai)
        db.session.commit()

    subject_codes = [
        "AUIUI/AP1FS",
        "AUIUI/AP1FY",
        "AUM/AP1MS",
        "AUPKS/AP1MD",
        "AUPKS/AP1DS",
        "AUIUI/AP2PN",
        "AUIUI/AP2TP",
        "AUIUI/AP2CC",
        "AUM/AP2AS",
        "AUPKS/AP2AE",
        "AUPKS/AP2MG",
        "AUIUI/AP3AL",
        "AUIUI/AP3KR",
        "AUIUI/AP3TI",
        "AUPKS/AP3OS",
        "AUPKS/AP3OV",
        "AUBI/AP4E0",
        "AUIUI/AP4ST",
        "AUIUI/AP4TS",
        "AUIUI/AP4TW",
        "AUM/AP4OM",
        "AUPKS/AP4AF",
        "AUART/AP5ES",
        "AUBI/AP5AC",
        "AUIUI/AP5PC",
        "AUPKS/AP6PP",
        "MUPE/AP6PE",
        "AUIUI/AP5PM",
        "AUIUI/AP5VS",
        "AUPKS/AP5PW",
        "AUIUI/AP6BS",
        "AUIUI/AP6UI",
    ]

    for code in subject_codes:
        existing = Subject.query.filter_by(code=code).first()
        if not existing:
            short_name = code.split("/")[-1]
            subject = Subject(
                name=short_name,
                code=code,
                faculty_id=fai.id
            )
            db.session.add(subject)

    db.session.commit()
    print("FAI subjects seeded successfully.")
