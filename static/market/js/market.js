$(function () {
    // 滚动条处理
    $('.market').width(innerWidth)


    // 获取下标 typeIndex
    var index = $.cookie('index')
    console.log(index)
    if(index){  // 存在，对应分类
        $('.type-slider li').eq(index).addClass('active')
    } else {    // 不存在，默认就是热榜
        $('.type-slider li:first').addClass('active')
    }

    //实现侧边栏黄条定位选中当前分类功能
    // 侧边栏点击处理 (页面会重新加载)
    $('.type-slider li').click(function () {
        // 保存下标
        // console.log($(this).index())
        // 保存下标 cookie
        $.cookie('index', $(this).index(),{exprires:3, path:'/'})
    })

    //子类
    var categoryShow = false
    $('#category-bt').click(function () {
        categoryShow = !categoryShow
        categoryShow?categoryShow():categoryHide()
    })

    function categoryViewShow(){
        $('.category-view').show()
        $('#category-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        sortViewHide()
        sortShow = false
    }

    function categoryViewHide(){
        $('.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }

    //排序
    var sortShow = false
    $('#sort-bt').click(function () {
        sortShow = !sortShow
        sortShow?sortViewShow():sortViewHide()
    })

    function sortViewShow(){
        $('.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        categoryViewHide()
        categoryShow = false
    }

    function sortViewHide(){
        $('.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }

    //灰色蒙层
    $('.bounce-view').click(function () {
        sortViewHide()
        sortShow= false

        categoryViewHide()
        categoryShow = false

    })
})