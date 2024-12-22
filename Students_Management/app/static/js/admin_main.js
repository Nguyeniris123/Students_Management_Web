//function addScore(studentId, scoreType) {
//    // Gửi yêu cầu đến server để thêm điểm
//    alert(`Thêm điểm cho học sinh ${studentId}, loại điểm: ${scoreType}`);
//}
//
//function editScore(scoreId) {
//    // Gửi yêu cầu đến server để sửa điểm
//    alert(`Sửa điểm có ID: ${scoreId}`);
//}
//
//function deleteScore(scoreId) {
//    // Gửi yêu cầu đến server để xóa điểm
//    alert(`Xóa điểm có ID: ${scoreId}`);
//}

function addScore(studentId, scoreType) {
    const newScore = prompt(`Nhập điểm mới cho loại điểm: ${scoreType}`);
    if (newScore) {
        // Gửi yêu cầu AJAX để thêm điểm
        fetch(`/add_score`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ student_id: studentId, score_type: scoreType, score: newScore }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Thêm điểm thành công!");
                location.reload();
            } else {
                alert("Có lỗi xảy ra.");
            }
        });
    }
}

function editScore(studentId, scoreType, oldScore) {
    const newScore = prompt(`Nhập điểm mới cho loại điểm: ${scoreType}`, oldScore);
    if (newScore) {
        // Gửi yêu cầu AJAX để sửa điểm
        fetch(`/edit_score`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ student_id: studentId, score_type: scoreType, old_score: oldScore, new_score: newScore }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Sửa điểm thành công!");
                location.reload();
            } else {
                alert("Có lỗi xảy ra.");
            }
        });
    }
}

function deleteScore(studentId, scoreType, score) {
    if (confirm(`Bạn có chắc muốn xóa điểm ${score} cho loại điểm: ${scoreType}?`)) {
        // Gửi yêu cầu AJAX để xóa điểm
        fetch(`/delete_score`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ student_id: studentId, score_type: scoreType, score: score }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Xóa điểm thành công!");
                location.reload();
            } else {
                alert("Có lỗi xảy ra.");
            }
        });
    }
}

