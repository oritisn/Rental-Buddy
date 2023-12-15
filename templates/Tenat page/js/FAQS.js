$(document).ready(function() {
    $('#faqs dt').click(function() {
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).next().slideUp();
        } else {
            $(this).siblings('dt').removeClass('active');
            $(this).addClass('active');
            $(this).next().slideDown().siblings('dd').slideUp();
        }
    });
});


