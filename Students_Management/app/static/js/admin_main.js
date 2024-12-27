function addStudent() {
    const name = document.getElementById('name').value;
    const gender = document.getElementById('gender').value;
    const birth = document.getElementById('birth').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value;

    // Kiểm tra dữ liệu nhập vào
    if (!name || !gender || !birth || !email || !phone || !address) {
        alert("Vui lòng điền đầy đủ thông tin.");
        return;
    }

    const data = {
        name: name,
        gender: gender,
        birth: birth,
        email: email,
        phone: phone,
        address: address
    };

    fetch('/admin/studentview/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        alert('Đã có lỗi xảy ra. Vui lòng thử lại.');
    });
}

function deleteStudent(studentId) {
    if (confirm("Bạn có chắc chắn muốn xóa học sinh này?")) {
        fetch(`/admin/studentview/delete_student/${studentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert('Đã có lỗi xảy ra. Vui lòng thử lại.');
        });
    }
}

function updateStudentClass(studentId) {
    if (confirm('Bạn có chắc muốn chuyển học sinh này sang lớp chưa xác định?')) {
        fetch(`/admin/studentview/update_student_class`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                student_id: studentId,
                new_class_id: 1, // Giá trị class_id mới là 1 (Lớp chưa xác định)
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // Cập nhật danh sách học sinh sau khi thay đổi
                location.reload();
            } else {
                alert(`Lỗi: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra khi chuyển lớp.');
        });
    }
}

function addStudentToClass() {
    const classId = document.getElementById("class").value;
    const studentId = document.getElementById("studentSelect").value;

    // Gửi yêu cầu AJAX để thêm học sinh vào lớp
    fetch(`/admin/studentview/add_student_to_class`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            class_id: classId
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();  // Làm mới trang để cập nhật danh sách
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        alert('Có lỗi xảy ra khi thêm học sinh vào lớp.');
    });
}

function updateStudentCount(classId) {
    // Gửi yêu cầu đến server để lấy sĩ số
    fetch(`/admin/studentclassview/student_count/${classId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('student-count').value = data.count;
            } else {
                alert("Lỗi: " + data.message);
            }
        })
        .catch(error => {
            console.error("Có lỗi xảy ra:", error);
        });
}

// Khi tải trang, lấy sĩ số cho lớp được chọn sẵn
document.addEventListener("DOMContentLoaded", function () {
    const classId = document.getElementById('class').value;
    if (classId) {
        updateStudentCount(classId);
    }
});


function addScore(studentId, scoreType) {
    const scoreValue = prompt("Nhập điểm cần thêm:");

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
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        alert('Không thể thêm điểm. Vui lòng thử lại.');
    });
}


function editScore(scoreId, currentValue) {
    const newScore = prompt('Nhập điểm mới:', currentValue);

    if (newScore !== null) {
        fetch('/admin/scoreview/edit_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ score_id: scoreId, new_value: parseFloat(newScore) }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // Tải lại trang
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert('Không thể sửa điểm. Vui lòng thử lại.');
        });
    }
}


function deleteScore(scoreId) {
    if (confirm("Bạn có chắc chắn muốn xóa điểm này không?")) {
        fetch('/admin/scoreview/delete_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ score_id: scoreId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // Tải lại trang để cập nhật danh sách điểm
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert("Không thể xoá điểm. Vui lòng thử lại.");
        });
    }
}



