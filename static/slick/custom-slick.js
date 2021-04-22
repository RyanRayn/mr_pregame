/* Custom settings for carousel on matchup page */

$(document).ready(function(){
    $('.slick-slider').slick({
        autoplay:true,
        autoplaySpeed:3000,
        infinite:true,
        slidesToShow:1,
        pauseOnHover:true,
        fade:true,
        arrows: true,
        prevArrow: '<div class="arrow-prev"><i class="fas fa-chevron-left orange"></i></div>',
        nextArrow: '<div class="arrow-next"><i class="fas fa-chevron-right orange"></i></div>',
    });
});