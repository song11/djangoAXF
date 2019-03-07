$(function () {
    // 为了隐藏滚动条
    $('.home').width(innerWidth)

    var topSwiper = new Swiper('#topSwiper', {
        // slidesPerView: 1,
        // spaceBetween: 30,
        // autoplay: 2500,
        // // loop: true,
        // pagination: '.swiper-pagination',

        pagination: '.swiper-pagination',
        // nextButton: '.swiper-button-next',
        // prevButton: '.swiper-button-prev',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween: 30,
        loop: true,
        autoplay: 3000,
        effect: 'coverflow',

    });


    var mustbuySwiper = new Swiper('#mustbuySwiper', {
        slidesPerView: 3,
        spaceBetween: 5,
        loop: true,
    })


})