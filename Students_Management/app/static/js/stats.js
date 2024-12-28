function create_chart(labels, data, background_colors) {
    canvas = document.createElement('canvas')
    canvas.id = 'statsChart'

    chart_container = document.getElementById('chart_container')
    chart_container.innerHTML = ""
    chart_container.appendChild(canvas)

    const ctx = canvas.getContext('2d')
    const myChart =  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lượng học sinh đạt',
        data: data,
        backgroundColor: background_colors,
        borderWidth: 1,
        barThickness: 30
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function send_request_stats() {
    semester = document.getElementById('semester_id')
    semester_id = semester.value
    selectedSubject = document.getElementById('subject_id')
    subject_id = selectedSubject.value

    fetch('api/reload_table',{
        method: 'post',
        body: JSON.stringify({
            'semester_id' : semester_id,
            'subject_id' : subject_id
        }),
        headers: {
            'Content-type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(new_table) {
        let labels = []
        let data = []
        let background_colors = []
        let r = Math.floor(Math.random() * 256);  // Red component (0-255)
        let g = Math.floor(Math.random() * 256);  // Green component (0-255)
        let b = Math.floor(Math.random() * 256);  // Blue component (0-255)
        const a = (Math.random() * 0.5 + 0.3).toFixed(2); // Alpha (opacity) between 0.3 and 0.8
        div_subject_name = document.getElementById('subject_name_id')
        div_semester_year = document.getElementById('semester_year_id')
        div_table_data = document.getElementById('table_data_id')
        div_subject_name.textContent = `Môn học: ${new_table['subject_name']}`
        div_semester_year.textContent = `Thời gian: ${new_table['semester_year']}`

        div_table_data.innerHTML = ""
         //STT, LOP ,SS ,SLD , TY LE
        new_avg_score = new_table['class_avg_score']
        for (let i = 0;i < new_avg_score.length;i++) {
            row = document.createElement('div')
            row.classList.add('row', 'm-0' ,'border-bottom')

            stt = document.createElement('div')
            stt.classList.add('col-md-1', 'col-1', 'text-center', 'p-2', 'border-left')
            stt.textContent = `${i+1}`

            lop = document.createElement('div')
            lop.classList.add('col-md-5', 'col-5', 'text-center', 'p-2', 'border-left')
            lop.textContent = new_avg_score[i][0]
            labels.push(lop.textContent)

            ss = document.createElement('div')
            ss.classList.add('col-md-2', 'col-2', 'text-center', 'p-2', 'border-left')
            ss.textContent = new_avg_score[i][1]

            sld = document.createElement('div')
            sld.classList.add('col-md-2', 'col-2', 'text-center', 'p-2', 'border-left')
            sld.textContent = new_avg_score[i][2]
            data.push(new_avg_score[i][2])

            tyLe = document.createElement('div')
            tyLe.classList.add('col-md-2', 'col-2', 'text-center', 'p-2', 'border-left')
            tyLe.textContent = Math.round((new_avg_score[i][2]/new_avg_score[i][1]) * 100)

            row.append(stt,lop,ss,sld,tyLe)
            div_table_data.appendChild(row)
            r = Math.floor(Math.random() * 256);
            g = Math.floor(Math.random() * 256);
            b = Math.floor(Math.random() * 256);
            background_colors.push(`rgba(${r}, ${g}, ${b}, ${a})`)
        }
          create_chart(labels,data,background_colors)
    })

}


function load_subject_data() {
    semester = document.getElementById('semester_id')
    semester_id = semester.value
    fetch('api/load_subject_data',{
        method: 'post',
        body: JSON.stringify({
            'semester_id' : semester_id
            }),
        headers: {
            'Content-type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data_subjects) {
       selectSubject = document.getElementById('subject_id');
       selectSubject.innerHTML = "";

       data_subjects.forEach(function(subject) {
            option = document.createElement('option')
            option_text_node = document.createTextNode(`${subject[1]}`)
            option.appendChild(option_text_node)
            option.value = `${subject[0]}`
            selectSubject.appendChild(option)
       })
       selectSubject.options[0].selected = true
       selectSubject.onchange()

    }).catch(function(err) {
        console.log(err);
    })
}
