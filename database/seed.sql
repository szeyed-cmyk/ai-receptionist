-- Optional demo data. Not required for the app to run.

INSERT INTO knowledge_items (question, answer, category, is_active, created_at)
VALUES
('What are your opening hours?', 'Monday to Saturday, 9 AM to 6 PM. Closed on Sunday.', 'general', 1, datetime('now')),
('Do you offer digital marketing?', 'Yes. Book a consultation from the chat.', 'services', 1, datetime('now'));

INSERT INTO settings (key, value) VALUES
('business_name', 'FrontDesk AI'),
('opening_hour', '9'),
('closing_hour', '18'),
('closed_days', 'sunday'),
('holiday_dates', '');
