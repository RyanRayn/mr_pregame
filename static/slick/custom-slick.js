
$(document).ready(function(){
    $('.slick-slider').slick({
        infinite:true,
        autoplay:true,
        autoplaySpeed: 3000,
        speed: 1000,
        arrows:false,
        slidesToShow: 12,
        slidesToScroll: 1,
        draggable:true,
        swipe:true,
        swipeToSlide:true,
        focusOnSelect:false,
        variableWidth: true,
        variableHeight: true,
        responsive: [
            {
            breakpoint:1650,
            settings: {
                centerMode:true,
                slidesToShow: 11,
                slidesToScroll: 1,
                infinite:true,
                autoplay:true,
                autoplaySpeed: 3000,
                arrows:false,
                draggable:true,
                swipe:true,
                swipeToSlide:true,
                focusOnSelect:false,
                variableWidth: true,
                variableHeight: true
            }
            },
            {
            breakpoint:1400,
            settings: {
                centerMode:true,
                slidesToShow: 9,
                slidesToScroll: 1,
                infinite:true,
                autoplay:true,
                autoplaySpeed: 3000,
                arrows:false,
                draggable:true,
                swipe:true,
                swipeToSlide:true,
                focusOnSelect:false,
                variableWidth: true,
                variableHeight: true
            }    
            },
            {
            breakpoint: 1120,
            settings: {
                centerMode:true,
                slidesToShow: 8,
                slidesToScroll: 1,
                infinite:true,
                autoplay:true,
                autoplaySpeed: 3000,
                arrows:false,
                draggable:true,
                swipe:true,
                swipeToSlide:true,
                focusOnSelect:false,
                variableWidth: true,
                variableHeight: true
            }
            },
            {
            breakpoint: 600,
            settings: {
                centerMode:true,
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite:true,
                autoplay:true,
                autoplaySpeed: 3000,
                arrows:false,
                draggable:true,
                swipe:true,
                swipeToSlide:true,
                focusOnSelect:false,
                variableWidth: true,
                variableHeight: true
            }
            },
        ]
    });
});