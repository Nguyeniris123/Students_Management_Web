-- Quy định: một năm học có 2 học kỳ, mỗi môn học có
-- - Tối thiếu 1 và tối đa 5 cột điểm 15 phút
-- - Tối thiểu 1 và tối đa 3 bài kiểm tra 1 tiết.
-- - Có 1 điểm thi cuối kỳ
DELIMITER $$
CREATE TRIGGER check_score_type_insert
BEFORE INSERT ON score
FOR EACH ROW
BEGIN
    DECLARE count_15p INT;
    DECLARE count_1tiet INT;
    DECLARE count_cuoi_ky INT;

    -- Đếm số lượng điểm 15 phút
    SELECT COUNT(*) INTO count_15p
    FROM score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p') AND count_15p >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 5 cột điểm 15 phút.';
    END IF;

    -- Đếm số lượng bài kiểm tra 1 tiết
    SELECT COUNT(*) INTO count_1tiet
    FROM score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet') AND count_1tiet >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 3 bài kiểm tra 1 tiết.';
    END IF;

    -- Đếm số lượng điểm cuối kỳ
    SELECT COUNT(*) INTO count_cuoi_ky
    FROM score
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
CREATE TRIGGER check_score_type_update
BEFORE UPDATE ON score
FOR EACH ROW
BEGIN
    DECLARE count_15p INT;
    DECLARE count_1tiet INT;
    DECLARE count_cuoi_ky INT;

    -- Đếm số lượng điểm 15 phút
    SELECT COUNT(*) INTO count_15p
    FROM score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem15p') AND count_15p > 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 5 cột điểm 15 phút.';
    END IF;

    -- Đếm số lượng bài kiểm tra 1 tiết
    SELECT COUNT(*) INTO count_1tiet
    FROM score
    WHERE student_id = NEW.student_id
      AND subject_id = NEW.subject_id
      AND score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet');

    IF NEW.score_type_id = (SELECT id FROM score_type WHERE name = 'diem1tiet') AND count_1tiet > 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Mỗi học sinh chỉ được tối đa 3 bài kiểm tra 1 tiết.';
    END IF;

    -- Đếm số lượng điểm cuối kỳ
    SELECT COUNT(*) INTO count_cuoi_ky
    FROM score
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

-- Kiểm tra điểm từ 0-10 mới được nhập vào
DELIMITER $$
CREATE TRIGGER check_score_insert
BEFORE INSERT ON score
FOR EACH ROW
BEGIN
    IF NEW.so_diem < 0 OR NEW.so_diem > 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Điểm số không hợp lệ. Điểm phải nằm trong khoảng từ 0 đến 10';
    END IF;
END$$
DELIMITER ;

-- Kiểm tra điểm có nằm từ 0-10 khi cập nhật
DELIMITER $$
CREATE TRIGGER check_score_update
BEFORE UPDATE ON score
FOR EACH ROW
BEGIN
    IF NEW.so_diem < 0 OR NEW.so_diem > 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Điểm số không hợp lệ. Điểm phải nằm trong khoảng từ 0 đến 10';
    END IF;
END$$
DELIMITER ;

-- Năm của học kỳ và năm của khối lớp phải trùng nhau khi tạo hoặc chỉnh sửa môn học (Subject)
DELIMITER $$
CREATE TRIGGER subject_year_insert
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
CREATE TRIGGER subject_year_update
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

DELIMITER $$
CREATE TRIGGER check_student_age_insert
BEFORE INSERT ON student
FOR EACH ROW
BEGIN
    DECLARE student_birth DATE;
    DECLARE student_age INT;
    DECLARE min_age_student INT;
    DECLARE max_age_student INT;

    -- Lấy ngày sinh từ bảng User
    SELECT birth INTO student_birth FROM user WHERE id = NEW.id;

    -- Lấy giới hạn tuổi từ RegulationAge
    SELECT min_age, max_age 
    INTO min_age_student, max_age_student
    FROM regulation_age
    WHERE id = NEW.regulation_age_id;

    -- Tính tuổi
    SET student_age = TIMESTAMPDIFF(YEAR, student_birth, CURDATE());

    -- Kiểm tra tuổi
    IF student_age < min_age_student OR student_age > max_age_student THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Tuổi học sinh không hợp lệ. Tuổi phải nằm trong khoảng quy định.';
    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER check_student_age_update
BEFORE UPDATE ON user
FOR EACH ROW
BEGIN
    DECLARE student_age INT;
    DECLARE min_age_student INT;
    DECLARE max_age_student INT;

        -- Lấy giới hạn tuổi từ RegulationAge thông qua regulation_age_id
        SELECT min_age, max_age 
        INTO min_age_student, max_age_student
        FROM regulation_age
        WHERE id = (SELECT regulation_age_id FROM student WHERE id = OLD.id);

        -- Tính tuổi dựa vào ngày sinh mới
        SET student_age = TIMESTAMPDIFF(YEAR, NEW.birth, CURDATE());

        -- Kiểm tra độ tuổi có nằm trong khoảng quy định hay không
        IF student_age < min_age_student OR student_age > max_age_student THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ngày sinh không hợp lệ. Tuổi phải nằm trong khoảng quy định.';
        END IF;
END$$
DELIMITER ;


-- DROP TRIGGER IF EXISTS check_score_type_insert;
-- DROP TRIGGER IF EXISTS check_score_type_update;

-- DROP TRIGGER IF EXISTS check_score_insert;
-- DROP TRIGGER IF EXISTS check_score_update;

-- DROP TRIGGER IF EXISTS subject_year_insert;
-- DROP TRIGGER IF EXISTS subject_year_update;

-- DROP TRIGGER IF EXISTS check_student_age_insert;
-- DROP TRIGGER IF EXISTS check_student_age_update;


