function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function openForm1() {
    document.getElementById("comments").style.display = "block";
    document.getElementById("comments_cancel").style.display = "block";
}

function closeForm1() {
    document.getElementById("comments").style.display = "none";
    document.getElementById("comments_cancel").style.display = "none";
}




//const signInBtn = document.querySelector('.block');
//const signUpBtn = document.querySelector('.block_news');
//const formBox = document.querySelector('.block_box');
//const body = document.body;
//
//signUpBtn.addEventListener('click', function () {
//    formBox.classList.add('active');
//    body.classList.add('active');
//
//});
//
//signInBtn.addEventListener('click', function () {
//    formBox.classList.remove('active');
//    body.classList.remove('active');
//});



const part = '.part';
const part_active = 'part_active';
const button = '.button';

$(button).on('click', function() {
  $(this).parent(part).removeClass(part_active);
  var next = $(this).parent(part).next(part);
  if (next.length == 0)
    next = $(this).closest('.wrapper').find('.part').eq(0);
  next.addClass(part_active);
});