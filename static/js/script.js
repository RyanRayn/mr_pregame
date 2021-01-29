
/* 'base.html' - toggle plus/minus icon in navbar */
$('.navbar-toggler').click(function() { 
    $(this).find('i').toggleClass('fas fa-plus-circle fas fa-minus-circle'); 
});