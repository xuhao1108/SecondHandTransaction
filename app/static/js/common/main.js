$('#user_dropdown').hover(function () {
    $('#user_menu').css('display', 'block');
}, function () {
    $('#user_menu').css('display', 'none');
})

$('#about_dropdown').hover(function () {
    $('#about_menu').css('display', 'block');
}, function () {
    $('#about_menu').css('display', 'none');
})

$('li[catagory]').hover(function () {
    let c_id = this.getAttribute('catagory')
    $('ul[catagory=' + c_id + ']').css('display', 'block')
    // $('#about_menu').css('display', 'block');
}, function () {
    let catagory_id = this.getAttribute('catagory')
    $('ul[catagory=' + catagory_id + ']').css('display', 'none')
    // $('#about_menu').css('display', 'none');
})