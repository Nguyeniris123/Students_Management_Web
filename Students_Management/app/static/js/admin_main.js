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
        alert(data.message);
        if (data.success) {
            location.reload();
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
            alert(data.message);
            if (data.success) {
                location.reload(); // Tải lại trang
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
            alert(data.message);
            if (data.success) {
                location.reload(); // Tải lại trang để cập nhật danh sách điểm
            }
        })
        .catch(error => {
            alert("Đã xảy ra lỗi khi xóa điểm.");
        });
    }
}

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


