users
    id (PK)
    email (unique)
    created_at

requests (primary resource)
    id (PK)
    user_id (FK → users.id, nullable for now)
    input_text
    output_text
    created_at