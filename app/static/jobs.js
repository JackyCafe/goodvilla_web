var startTime, endTime;
var job_user;
var postData={}
var jsonData
var detail
var selectedDivs = []; // 用于存储已选中的<div>元素

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

/*載入sub item */
function load_subitem(param){
    $.ajax(
        {
            method:'GET',
            url: '/app/api/subitem/'+param+"/",
            success:function(result){

                var subitem =$('#subitem')
                html = ''
                $.each(result, function (index, item) {
                    html += '<btn class="m-1 btn btn-light btn-outline-primary" onClick="load_detail('+item.id+')">' + item.sub_items + '</btn>';
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
                html = ''
                $.each(result, function (index, item) {
                    html += '<btn class="m-1 btn btn-light btn-outline-primary" onClick="load_record('+item.id+')">' + item.detail + '</btn>';
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
    //todo 要改寫為POST
    if (selectedDivs.length==2){
        $('#workRecordForm').show();
        detail = param
    }else{
        alert('請選擇時間');
    }

}
/* getCookie 抓 csrf token
* */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function save(param){
    var csrftoken = getCookie('csrftoken');
    var now = new Date()
    var Today = now.getFullYear()+"-"+(now.getMonth())+"-"+now.getDate()
    console.log(Today)
    var spend_time =  calculateTimeDifference(startTime,endTime)
    var selectedValue=0
    var radioButtons = $('.form-check-input');
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            selectedValue = radioButtons[i].value;
             // 可以在这里使用选中的值执行其他操作
            break; // 如果只需要获取第一个选中的值，可以使用break
        }
    }
    postData.detail =detail
    postData.user=job_user
    postData.working_date="2024-01-10"
    postData.start_time = startTime
    postData.end_time = endTime
    postData.spend_time = spend_time
    postData.mood = selectedValue
    postData.bonus = $('#bonus').val()
    jsonData = JSON.stringify(postData)
    console.log(jsonData)



    //发送POST请求
    fetch('/app/api/workrecord/1/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: jsonData,
        //protocol: 'HTTP/2.0',
    })
    .then(response => {
        console.log(response.status)
        if (response.status === 201) {
            console.log('工作记录创建成功');
            inform();
            // 可以在这里处理成功后的逻辑
        } else {
            console.error(response.json);
            // 可以在这里处理失败后的逻辑
        }
    })
    .catch(error => {
        console.error('请求错误:', error);
    })
    // inform();
}



$(document).ready(
    function(){
    $('#workRecordForm').hide();

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
            if (selectedDivs.length === 2) {
                // 记录starttime和endtime
                startTime = selectedDivs[0].text();
                endTime = selectedDivs[1].text();
                var start = $('#start-time')
                var end = $('#end-time')
                start.html(startTime+"-"+endTime)
            }
        }
    )
});


function inform(user_id){
    var now = new Date()
    var Today = now.getFullYear()+"-"+(now.getMonth()+1)+"-"+now.getDate()
    console
    $.ajax(
        {
            method:'GET',
            url: '/app/api/summary/'+user_id+"/"+"2024-01-10"+"/",

            success:function(result){

                var report=$('#report')
                html='<table border=1> <tr><th>項目</th> <th>工時</th> <th>收益</th> </tr>'
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







