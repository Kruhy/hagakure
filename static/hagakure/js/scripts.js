$(".reveal").on('click',function() {
    var pwd = this.parentElement.parentElement.querySelector('.pwd');
    if (pwd.type === 'password') {
        pwd.type = 'text';
    } else {
        pwd.type = 'password';
    }
    var eye = this.parentElement.parentElement.querySelector('#eye');
    if (eye.className === 'fa fa-eye') {
        eye.className = 'fa fa-eye-slash';
    } else {
        eye.className = 'fa fa-eye';
    }
    console.log(eye)
});