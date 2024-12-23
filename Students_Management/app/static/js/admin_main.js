function addScore(studentId, scoreType) {
    const scoreValue = prompt("Nhập điểm cần thêm:");
    if (!scoreValue) {
        alert("Bạn chưa nhập điểm.");
        return;
    }

    fetch('/admin/scoreview/add_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            student_id: studentId,
            subject_id: document.getElementById("subject").value,
            score_type: scoreType,
            score_value: parseFloat(scoreValue)
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Lỗi:', error);
        alert('Không thể thêm điểm. Vui lòng thử lại.');
    });
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

