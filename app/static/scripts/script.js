$('.btn-friends').on('click', function() {
    $('.menu-friends').toggleClass('menu-active');
    $('.menu-messages').removeClass('menu-active');
})

$('.btn-messages').on('click', function() {
    $('.menu-messages').toggleClass('menu-active');
    $('.menu-friends').removeClass('menu-active');
})

$('.icon').on('click', function() {
    if ($(this).hasClass('icon-active')) {
        $('.icon').removeClass('icon-active')
    } else {
        $('.icon').removeClass('icon-active')
        $(this).toggleClass('icon-active')
    }
    
})

$('.login-form').on('click', function() {
    $(this).toggleClass('login-form-active');
})