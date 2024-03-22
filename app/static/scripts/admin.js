function showDiv(div_id) {
    document.getElementById("loginFormDiv").style.display = "none";
    document.getElementById("createUserFormDiv").style.display = "none";
    document.getElementById("createQuestionFormDiv").style.display = "none";
    document.getElementById("question-datalist").style.display = "none";
    document.getElementById("answer-datalist").style.display = "none";
    document.getElementById("user-datalist").style.display = "none";

    document.getElementById(div_id).style.display = "block";
}

function showCreateUserForm(){
    showDiv('createUserFormDiv');
}

function showCreateQuestionForm(){
    showDiv('createQuestionFormDiv');
}

function showQuestionList(){
    showDiv('question-datalist');
}

function showAnswerList(){
    showDiv('answer-datalist');
}

function showUserList(){
    showDiv('user-datalist');
}

function getToken(){
    return sessionStorage.getItem('token');
}

document.getElementById('q_data').addEventListener('click', showQuestionList);
document.getElementById('a_data').addEventListener('click', showAnswerList);
document.getElementById('u_data').addEventListener('click', showUserList);

function getAnswerCheckedIds() {
    var checkedIds = [];
    var checkboxes = document.querySelectorAll('.answer_checkbox:checked');
    checkboxes.forEach(function(checkbox) {
        var id = checkbox.closest('tr').querySelector('td:nth-child(2)').textContent;
        checkedIds.push(id);
    });
    return checkedIds;
}

function getQuestionChekedIds(){
    var checkedIds = [];
    var checkboxes = document.querySelectorAll('.question_checkbox:checked');
    checkboxes.forEach(function(checkbox) {
        var id = checkbox.closest('tr').querySelector('td:nth-child(2)').textContent;
        checkedIds.push(id);
    });
    return checkedIds;
}



document.getElementById("createUserForm").addEventListener("submit", function(event){
    event.preventDefault();
    var username = document.getElementById("createUsername").value;
    var password = document.getElementById("createPassword").value;
    var age = document.getElementById("createAge").value;
    var gender = document.getElementById("createGender").value;
    createUser(username, password, age, gender);
    showQuestionList();
    loaction.reload();  
})

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("admin_username").value;
    var password = document.getElementById("admin_password").value;
    login(username, password);
    })

    if (sessionStorage.getItem("token")){
        showQuestionList()
    }

function login(username, password){
    fetch('/admin/token',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        // 서버에서 응답 데이터로 받은 토큰을 세션 저장소에 저장
        sessionStorage.setItem('token',data.access_token);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
}

function createUser(username, password, age, gender){
    fetch('/admin/user',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            username: username,
            password: password,
            age: age,
            gender: gender
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(msg)
    })
    .catch(error => {
        console.error('Error: ', error);
    });

}

function getUserChekedIds(){
    var checkedIds = [];
    var checkboxes = document.querySelectorAll('.user_checkbox:checked');
    checkboxes.forEach(function(checkbox) {
        var id = checkbox.closest('tr').querySelector('td:nth-child(2)').textContent;
        checkedIds.push(id);
    });
    return checkedIds;
}

function delete_user(){
    ids = getUserChekedIds();
    ids.forEach(function(userid){
        deleteUser(userid);
    })
    location.reload();
}

function deleteUser(userid){
    fetch(`/admin/user/${userid}`,{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(msg);
    })
    .catch(error => {
        console.error('Error: ', error);
    })
}

document.getElementById("createQuestionForm").addEventListener("submit", function(event){
    event.preventDefault();
    var question = document.getElementById("question_text").value;
    createQuestion(question);

})

function createQuestion(question){
    fetch('/admin/questions',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            content: question
        })
    })
    .then(response => response.json())
    .then(data => {
        showQuestionList()
        loaction.reload()
    })
    .catch(error => {
        console.log('Error: ', error);
    })
}

function getQuestionChekedIds(){
    var checkedIds = [];
    var checkboxes = document.querySelectorAll('.question_checkbox:checked');
    checkboxes.forEach(function(checkbox) {
        var id = checkbox.closest('tr').querySelector('td:nth-child(2)').textContent;
        checkedIds.push(parseInt(id));
    });
    return checkedIds;
}

function delete_question(){
    ids = getQuestionChekedIds();
    ids.forEach(function(questionid){
        deleteQuestion(questionid);
    })
    location.reload();
}

function deleteQuestion(questionid){
    fetch(`/admin/questions/${questionid}`,{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        alert(data.msg);
    })
    .catch(error => {
        console.error('Error: ', error);
    })
}

function activate_question(){
    var questionids = getQuestionChekedIds();
    activateQuestion(questionids);
    location.reload();
}

function activateQuestion(questionids){
    fetch('/admin/questions/activate',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            question_ids: questionids
        })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error: ', error);
    })
}

function getAnswerChekedIds(){
    var checkedIds = [];
    var checkboxes = document.querySelectorAll('.answer_checkbox:checked');
    checkboxes.forEach(function(checkbox) {
        var id = checkbox.closest('tr').querySelector('td:nth-child(2)').textContent;
        checkedIds.push(id);
    });
    return checkedIds;
}

function delete_answer(){
    var ids = getAnswerChekedIds();
    deleteAnswers(ids);
    location.reload();
}

function deleteAnswers(answerids){
    fetch(`/admin/answers`,{
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getToken()
        },
        body: JSON.stringify({
            answer_ids: answerids
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Selected answers were successfully deleted')
        }
    })
    .catch(error => {
        console.error('Error: ', error);
    })
}