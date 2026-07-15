ALTER TABLE enrollments
ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'draft';

ALTER TABLE enrollments
DROP CONSTRAINT IF EXISTS ck_enrollments_status;

ALTER TABLE enrollments
ADD CONSTRAINT ck_enrollments_status
CHECK (status IN ('draft', 'submitted'));
