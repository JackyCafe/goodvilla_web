
let startTime, endTime;
let job_user;
const postData = {};
let jsonData;
let detail;
let selectedDivs = []; // 用于存储已选中的<div>元素

function calculateTimeDifference(start_time, end_time)  {
    const startTimeArray = start_time.split(':');
    const endTimeArray = end_time.split(':');
    const start = new Date();
    start.setHours(parseInt(startTimeArray[0]), parseInt(startTimeArray[1]), 0, 0);
    const end = new Date();
    end.setHours(parseInt(endTimeArray[0]), parseInt(endTimeArray[1]), 0, 0);
    const timeDifference = end.getTime() - start.getTime();
    const hours = Math.floor(timeDifference / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    return hours*60+minutes;
  }

function loadJobs(user) {
    job_user = user;
}

/*
   載入次要選單
** */
function load_subitem(param){
    $.ajax(
        {
            method:'GET',
            url: '/app/api/subitem/'+param+"/",
            success:function(result){
                const subitem = $('#subitem');
                let html = ''
                $.each(result, function (index, item) {
                    html += '<btn class="m-1 btn btn-light btn-outline-primary" ' +
                        'onClick="load_detail('+item.id+')">' + item.sub_items + '</btn>';
                });
                subitem.html(html)
            },
            error:function(){
                console.error('error'+param);
            }
        }
    );
}

/*載入detail */
function load_detail(param){
    $.ajax(
        {
            method:'GET',
            url: '/app/api/detail/'+param+"/",
            success:function(result){

                var detail =$('#detail')
                let html = ''
                $.each(result, function (index, item) {
                    html += '<btn class="m-1 btn btn-light btn-outline-primary" ' +
                        'onClick="load_record('+item.id+')">' + item.detail + '</btn>';
                });
                detail.html(html)
            },
            error:function(){
                console.error('error'+param);
            }
        }
    );
}
/**寫入record */
function load_record(param){
    if (selectedDivs.length===2){
        $('#workRecordForm').show();
        detail = param
    }else{
        alert('請選擇時間');
    }

}
/* getCookie 抓 csrf token
* */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function todo_add(){
   /*** 新增待辦事項
    */
    const csrftoken = getCookie('csrftoken');
    const text = $('#todo_area').val()
    postData.todo_user = job_user
    postData.todo_text=text
    jsonData = JSON.stringify(postData)
    console.log(jsonData)
    fetch('/app/api/todo/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken':csrftoken,
            },
            body: jsonData,}).then(response => {
        if (response.status === 201) {
            alert("新增完成")
            selectedDivs = []
        } else {
            console.error(response.json);
            // 可以在这里处理失败后的逻辑
        }
    })


}
// 選完後 Insert
//
function save(param){
    /** 將每個時段的資料寫入
    * */
    const csrftoken = getCookie('csrftoken');
    // 抓系統時間，要將今天資料寫入db
    const now = new Date();
    // 系統抓的月份會少1
    const Today = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate();
    // 透過calculateTimeDifference 函數抓時間差
    const spend_time = calculateTimeDifference(startTime, endTime);
    let selectedValue = 0;
    const radioButtons = $('.form-check-input');
    // 心情指數，用radio button 控制
    for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            selectedValue = radioButtons[i].value;
            break; // 如果只需要获取第一个选中的值，可以使用break
        }
    }
    postData.detail =detail
    postData.user=job_user
    postData.working_date=Today
    postData.start_time = startTime
    postData.end_time = endTime
    postData.spend_time = spend_time
    postData.mood = selectedValue
    postData.bonus = $('#bonus').val()
    jsonData = JSON.stringify(postData)
    console.log(jsonData)

    fetch('/app/api/working/'+job_user+'/'+Today+'/'+startTime+"/"+endTime+"/")
        .then(response=>response.json())
        .then(data=>{
            if (data==="1"){
                //发送POST请求
                fetch('/app/api/workrecord/1/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken':csrftoken,
                     },
                    body: jsonData,
                }).then(response => {
                    if (response.status === 201) {
                        alert("新增完成")
                        selectedDivs = []
                    } else {
                        console.error(response.json);
            // 可以在这里处理失败后的逻辑
                }
                }).then(
                    response=>{
                        inform(job_user)
                }
                ).catch(error => {
                     console.error('请求错误:', error);})
            }else {
                alert("該時段已有資料")
            }
        })

    // inform();
}

function todo_form(){
    $('#todo').toggle();


}


function createToast(msg) {

  }

  // 調用createToast函數以顯示Toast
function strToMin(timeString) {
    // 将时间字符串拆分为小时和分钟
    let [hours, minutes] = timeString.split(':').map(Number);

    // 将小时转换为分钟并加上分钟数
    let totalMinutes = hours * 60 + minutes;

    return totalMinutes;
    }

$(document).ready(

    function(){
    $('#workRecordForm').hide();
    $('#todo').hide()


    $('.timer').click(
        function(){
            var div =$(this);
            if(div.hasClass('selected')){
                div.removeClass('selected');
                selectedDivs.pop();
            }else{
                if (selectedDivs.length==2){
                    var firstSelectedDiv = selectedDivs.shift();
                    firstSelectedDiv.removeClass('selected');
                }
                div.addClass('selected')
                selectedDivs.push(div);
                $('#workRecordForm').hide();
            }

            /* 修正日期先後關係*/
            if (selectedDivs.length === 2) {
                // 记录starttime和endtime
                t1 = selectedDivs[0].text();
                t2 = selectedDivs[1].text();
                console.log(strToMin(t1))
                console.log(strToMin(t2))
                startTime = strToMin(t1)<strToMin(t2)?t1:t2
                endTime = strToMin(t1)>strToMin(t2)?t1:t2
                console.log(startTime)

                var start = $('#start-time')


                start.html(startTime+"-"+endTime)
            }
        }
    )
    function toTime(timeString){
        const today = new Date();
        const [hours, minutes] = timeString.split(':');
        return new Date(
            today.getFullYear(),
            today.getMonth(),
            today.getDate(),
            hours, minutes
        );
    }

    let firstClick = 0;
    let secondClick =0;
    $('.grid-item').click(function () {
        const div = $(this);
        if (selectedDivs.length===2){
            firstClick = toTime(startTime)
            secondClick = toTime(endTime)
            $('.grid-item').each(function (){
                const itemTime = toTime($(this).text())
                if (itemTime >= firstClick && itemTime <= secondClick) {
                    $(this).css('background-color', 'yellow');
                }
            })
        }

    })



});


function inform(user_id){
    var now = new Date()
    var Today = now.getFullYear()+"-"+(now.getMonth()+1)+"-"+now.getDate()
    $.ajax(
        {
            method:'GET',
            url: '/app/api/summary/'+user_id+"/"+Today+"/",

            success:function(result){

                var report=$('#report')
                html='<table border=1 class="table"> <tr><th>項目</th> <th>工時</th> <th>收益</th> </tr>'
                $.each(result, function (index, item) {
                    html +='<tr><td>'+item.item+'</td><td>'+item.daily_spend+'</td><td>'+item.daily_bonus+'</td></tr>'

                });
                html+="</table>"
                report.html(html)

            },

            error:function(){
                console.error('error'+error);
                alert(error)
            }
        }
    );
}
