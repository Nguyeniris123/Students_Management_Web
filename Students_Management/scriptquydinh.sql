-- Quy định: một năm học có 2 học kỳ, mỗi môn học có
-- - Tối thiếu 1 và tối đa 5 cột điểm 15 phút
-- - Tối thiểu 1 và tối đa 3 bài kiểm tra 1 tiết.
-- - Có 1 điểm thi cuối kỳ
DELIMITER $$
CREATE TRIGGER trg_check_scores_insert
BEFORE INSERT ON Score
FOR EACH ROW
BEGIN
    DECLARE count_15p INT;
    DECLARE count_1tiet INT;
    DECLARE count_cuoi_ky INT;

    -- Đếm số lượng điểm 15 phút
    SELECT COUNT(*) INTO count_15p
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p') AND count_15p >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 5 cột điểm 15 phút.';
    END IF;

    -- Đếm số lượng bài kiểm tra 1 tiết
    SELECT COUNT(*) INTO count_1tiet
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet') AND count_1tiet >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 3 bài kiểm tra 1 tiết.';
    END IF;

    -- Đếm số lượng điểm cuối kỳ
    SELECT COUNT(*) INTO count_cuoi_ky
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diemck');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diemck') AND count_cuoi_ky >= 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 1 điểm thi cuối kỳ.';
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_check_scores_update
BEFORE UPDATE ON Score
FOR EACH ROW
BEGIN
    DECLARE count_15p INT;
    DECLARE count_1tiet INT;
    DECLARE count_cuoi_ky INT;

    -- Đếm số lượng điểm 15 phút
    SELECT COUNT(*) INTO count_15p
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p') AND count_15p >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 5 cột điểm 15 phút.';
    END IF;

    -- Đếm số lượng bài kiểm tra 1 tiết
    SELECT COUNT(*) INTO count_1tiet
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet') AND count_1tiet >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 3 bài kiểm tra 1 tiết.';
    END IF;

    -- Đếm số lượng điểm cuối kỳ
    SELECT COUNT(*) INTO count_cuoi_ky
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diemck');

    -- Nếu loại điểm cũ không phải là diemck và loại điểm mới là diemck
    IF OLD.score_type_id <> (SELECT id FROM score_type WHERE name = 'diemck')
       AND NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diemck')
       AND count_cuoi_ky >= 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ có 1 điểm thi cuối kỳ duy nhất.';
    END IF;

END$$
DELIMITER ;

DROP TRIGGER IF EXISTS trg_check_scores_insert;
DROP TRIGGER IF EXISTS trg_check_scores_update;

SHOW TABLES;


