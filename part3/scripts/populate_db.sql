SQL_POPULATE_DATA = """
-- Insert admin user (password will be hashed by application)
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Admin',
    'HBnB',
    'admin@hbnb.com',
    'hashed_password_here', -- This should be replaced with actual hash
    TRUE,
    datetime('now'),
    datetime('now')
);

-- Insert sample amenities
INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at) VALUES
('a1111111-1111-1111-1111-111111111111', 'WiFi', datetime('now'), datetime('now')),
('a2222222-2222-2222-2222-222222222222', 'Air Conditioning', datetime('now'), datetime('now')),
('a3333333-3333-3333-3333-333333333333', 'Swimming Pool', datetime('now'), datetime('now')),
('a4444444-4444-4444-4444-444444444444', 'Gym', datetime('now'), datetime('now')),
('a5555555-5555-5555-5555-555555555555', 'Parking', datetime('now'), datetime('now')),
('a6666666-6666-6666-6666-666666666666', 'Pet Friendly', datetime('now'), datetime('now')),
('a7777777-7777-7777-7777-777777777777', 'Kitchen', datetime('now'), datetime('now')),
('a8888888-8888-8888-8888-888888888888', 'Washing Machine', datetime('now'), datetime('now')),
('a9999999-9999-9999-9999-999999999999', 'TV', datetime('now'), datetime('now')),
('a0000000-0000-0000-0000-000000000000', 'Balcony', datetime('now'), datetime('now'));

-- Insert sample regular user
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    'John',
    'Doe',
    'john.doe@example.com',
    'hashed_password_here', -- This should be replaced with actual hash
    FALSE,
    datetime('now'),
    datetime('now')
);
"""
