$('#datepicker').datepicker({
    format: 'dd-mm-yyyy'  
});

<<<<<<< Updated upstream
$(document).ready(function() {
    console.log("jQuery is working!");
});

// var input = document.getElementById('inputsearch')
// var btn_search = document.getElementById('btn_search')

// input.oninput = () => {
//     btn_search.click()
// }
=======
            body.classList.toggle('bg-dark');
            body.classList.toggle('text-red');
            header.classList.toggle('bg-dark');
            header.classList.toggle('text-white');
            footer.classList.toggle('bg-dark');
        });



function selectYear(Object){
    fetch(`/lookuppoints/year/${parseInt(Object.value)}`, {
        method: "get",
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        let selecter = document.getElementById("semester");
        let array = ""
        for(let i=0; i < data["semesters_id"].length; i++){
            array += `<option value="${data["semesters_id"][i]}" {% if ${data["semesters_id"][i]} == request.args.get('semester') %} selected {% endif %}>${data["semesters_name"][i]}</option>`
        }
        selecter.innerHTML = array;
    })
}

function load_regulation(regulation_id){
    fetch(`/regulationtostudent/${regulation_id}`, {
        method: "get",
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        let regulation = document.getElementById("contain_model_regulations")
        let array = `<div class="modal fade" id="${data["id"]}" tabindex="-1" aria-labelledby="${data["id"]}Label" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="${data["id"]}Label">Quy Định về ${data["name"]}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>
                    ${data["max_students"] ?
                                    `Sỉ số tối đa của 1 lớp là ${data["max_students"]}` :
                                    `Độ tuổi tiếp nhận học sinh là từ ${data["min_age"]} đến ${data["max_age"]}`
                                }
                </p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
            </div>
        </div>
    </div>
</div>`
        regulation.innerHTML = array
    })
}

>>>>>>> Stashed changes
