INSERT INTO user (username, password)
VALUES
  ('test', '$2b$12$l0RHIWeuPt3gIFFjW1VGtOpvWnltkint1ds0LQT2n.dhIT9RjRxHS'),
  ('other', '$2b$12$KEzeNhNqHbD.6zunLXh8IeQQrnq6jZ3vr.qXRHRRDFQ/SvL7t59GS');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
