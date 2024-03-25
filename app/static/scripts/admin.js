if (sessionStorage.getItem("token")){
    showQuestionList();

    document.getElementById('q_data').addEventListener('click', function(){
        getAllQuestions();
        showQuestionList();
    })
    document.getElementById('a_data').addEventListener('click', function(){
        getAllAnswers();
        showAnswerList();
    })
    document.getElementById('u_data').addEventListener('click', function(){
        getAllUsers();
        showUserList();
    })

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

    document.getElementById("createQuestionForm").addEventListener("submit", function(event){
        event.preventDefault();
        var question = document.getElementById("question_text").value;
        createQuestion(question);

    })

    document.getElementById('question-search-form').addEventListener('submit', function(event){
        event.preventDefault();
        var keyword = document.getElementById('question-keyword').value;
        searchQuestion(keyword);
        showQuestionList();
    })

    document.getElementById('user-search-form').addEventListener('submit', function(event){
        event.preventDefault();
        var keyword = document.getElementById('user-keyword').value;
        searchUser(keyword);
        showUserList();
    })
}

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("admin_username").value;
    var password = document.getElementById("admin_password").value;
    login(username, password);

    })

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
        checkedIds.push(parseInt(id));
    });
    return checkedIds;
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

function delete_question(){
    ids = getQuestionChekedIds();
    ids.forEach(function(questionid){
        deleteQuestion(questionid);
    })
    location.reload();
}

function delete_answer(){
    var ids = getAnswerCheckedIds();
    deleteAnswers(ids);
    location.reload();
}

function activate_question(){
    var questionids = getQuestionChekedIds();
    activateQuestion(questionids);
    location.reload();
}

function deactivate_question(){
    var questionids = getQuestionChekedIds();
    deactivateQuestion(questionids);
    location.reload();
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
        if (sessionStorage.getItem("token")){
            showQuestionList()
        }
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

function deactivateQuestion(questionids){
    fetch('/admin/questions/deactivate',{
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

function searchQuestion(keyword) {
    fetch(`/admin/questions/search/${keyword}`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            let html = '';
            data.forEach(question => {
                html += `
                <tr>
                    <td>&nbsp&nbsp<input type="checkbox" class="question_checkbox"></td>
                    <td>${question.id}</td>
                    <td>${question.content}</td>
                    <td>${question.active}</td>
                </tr>`;
            });
            document.getElementById('question-data-table').innerHTML = html;
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}

function searchUser(keyword) {
    fetch('/admin/question', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            let html = '';
            data.forEach(user => {
                html += `
                <tr>
                    <td>&nbsp&nbsp<input type="checkbox" class="user_checkbox"></td>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.gender}</td>
                    <td>${user.age}</td>
                    <td>${user.is_superuser}</td>
                    <td>
                        <button type="button" class="btn btn-secondary">Details</button>
                    </td>
                </tr>`;
            });
            document.getElementById('user-data-table').innerHTML = html;
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}

function getAllQuestions() {
    fetch('/admin/questions', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            let html = '';
            data.forEach(question => {
                html += `
                <tr>
                    <td>&nbsp&nbsp<input type="checkbox" class="question_checkbox"></td>
                    <td>${question.id}</td>
                    <td>${question.content}</td>
                    <td>${question.active}</td>
                </tr>`;
            });
            document.getElementById('question-data-table').innerHTML = html;
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}

function getAllAnswers() {
    fetch('/admin/answers', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            let html = '';
            data.forEach(answer => {
                html += `
                <tr>
                    <td>&nbsp&nbsp<input type="checkbox" class="answer_checkbox"></td>
                    <td>${answer.id}</td>
                    <td>${answer.answer}</td>
                    <td>${answer.user_id}</td>
                    <td>${answer.question_id}</td>
                </tr>`;
            });
            document.getElementById('answer-data-table').innerHTML = html;
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}

function getAllUsers() {
    fetch('/admin/user', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            let html = '';
            data.forEach(user => {
                html += `
                <tr>
                    <td>&nbsp&nbsp<input type="checkbox" class="user_checkbox"></td>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.gender}</td>
                    <td>${user.age}</td>
                    <td>${user.is_superuser}</td>
                    <td>
                        <button type="button" class="btn btn-secondary">Details</button>
                    </td>
                </tr>`;
            });
            document.getElementById('user-data-table').innerHTML = html;
        })
        .catch(error => {
            console.error('Error: ', error);
        });
}