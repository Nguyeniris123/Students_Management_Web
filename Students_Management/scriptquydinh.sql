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

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p') AND count_15p > 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 5 cột điểm 15 phút.';
    END IF;

    -- Đếm số lượng bài kiểm tra 1 tiết
    SELECT COUNT(*) INTO count_1tiet
    FROM Score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet') AND count_1tiet > 3 THEN
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
    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diemck') AND count_cuoi_ky > 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ có 1 điểm thi cuối kỳ duy nhất.';
    END IF;
END$$
DELIMITER ;

-- Năm của học kỳ và năm của khối lớp phải trùng nhau khi tạo hoặc chỉnh sửa môn học (Subject)
DELIMITER $$
CREATE TRIGGER trg_validate_subject_year_insert
BEFORE INSERT ON subject
FOR EACH ROW
BEGIN
    DECLARE semester_year INT;
    DECLARE class_grade_year INT;

    -- Lấy năm của học kỳ
    SELECT year_id INTO semester_year
    FROM semester
    WHERE id = NEW.semester_id;

    -- Lấy năm của khối lớp
    SELECT year_id INTO class_grade_year
    FROM class_grade
    WHERE id = NEW.class_grade_id;

    -- Kiểm tra xem năm có trùng nhau hay không
    IF semester_year != class_grade_year THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Năm của học kỳ và năm của khối lớp không trùng nhau.';
    END IF;
END$$
DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_validate_subject_year_update
BEFORE UPDATE ON subject
FOR EACH ROW
BEGIN
    DECLARE semester_year INT;
    DECLARE class_grade_year INT;

    -- Lấy năm của học kỳ
    SELECT year_id INTO semester_year
    FROM semester
    WHERE id = NEW.semester_id;

    -- Lấy năm của khối lớp
    SELECT year_id INTO class_grade_year
    FROM class_grade
    WHERE id = NEW.class_grade_id;

    -- Kiểm tra nếu năm không khớp
    IF semester_year != class_grade_year THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Năm của học kỳ và năm của khối lớp không trùng nhau.';
    END IF;
END$$
DELIMITER ;

-- DELIMITER $$
-- CREATE TRIGGER check_student_age
-- BEFORE INSERT ON student
-- FOR EACH ROW
-- BEGIN
--     DECLARE student_age INT;
--     DECLARE min_age INT;
--     DECLARE max_age INT;

--     -- Tính tuổi của học sinh
--     SET student_age = TIMESTAMPDIFF(YEAR, NEW.birth, CURDATE());

--     -- Lấy giới hạn tuổi từ RegulationAge
--     SELECT min_age, max_age
--     INTO min_age, max_age
--     FROM regulation_age
--     WHERE id = NEW.regulation_age_id;

--     -- Kiểm tra tuổi
--     IF student_age < min_age OR student_age > max_age THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Tuổi học sinh không hợp lệ. Tuổi phải nằm trong khoảng quy định.';
--     END IF;
-- END$$
-- DELIMITER ;



-- DROP TRIGGER IF EXISTS trg_check_scores_insert;
-- DROP TRIGGER IF EXISTS trg_check_scores_update;
-- DROP TRIGGER IF EXISTS trg_validate_subject_year_insert;
-- DROP TRIGGER IF EXISTS trg_validate_subject_year_update;
-- DROP TRIGGER IF EXISTS check_student_age;


