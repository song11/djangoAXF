$(function () {
    // 滚动条处理
    $('.market').width(innerWidth)


    // 获取下标 typeIndex
    typeIndex = $.cookie('typeIndex')
    console.log(typeIndex)
    if(typeIndex){  // 存在，对应分类
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    } else {    // 不存在，默认就是热榜
        $('.type-slider .type-item:first').addClass('active')
    }


    // 侧边栏点击处理 (页面会重新加载)
    $('.type-slider .type-item').click(function () {
        // 保存下标
        // console.log($(this).index())
        // 保存下标 cookie
        $.cookie('typeIndex', $(this).index(),{exprires:3, path:'/'})
    })




    // 分类 和 排序
    var alltypeBt = false
    var sortBt = false
    $('#allBt').click(function () {
        // 取反
        alltypeBt = !alltypeBt

        if (alltypeBt){ // 显示
            $('.bounce-view.type-view').show()
            $('#allBt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

            sortBt = false
            $('.bounce-view.sort-view').hide()
            $('#sortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        } else {    // 隐藏
            $('.bounce-view.type-view').hide()
            $('#allBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
    })

    $('#sortBt').click(function () {
        // 取反
        sortBt = !sortBt

        if (sortBt){ // 显示
            $('.bounce-view.sort-view').show()
            $('#sortBt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

            alltypeBt = false
            $('.bounce-view.type-view').hide()
            $('#allBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        } else {    // 隐藏
            $('.bounce-view.sort-view').hide()
            $('#sortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
    })

    $('.bounce-view').click(function () {
        alltypeBt = false
        $('.bounce-view.type-view').hide()
            $('#allBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        sortBt = false
        $('.bounce-view.sort-view').hide()
        $('.bounce-view.sort-view').hide()
            $('#sortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    })



    // 购物车操作
    // 默认隐藏
    $('.bt-wrapper>.glyphicon-minus').hide()
    $('.bt-wrapper>.num').hide()

    // 购物车数据不为，即显示
    // each 遍历操作
    $('.bt-wrapper>.num').each(function () {
        if(parseInt($(this).html())){
            $(this).show()
            $(this).prev().show()
        }
    })
    
    // 加操作
    $('.bt-wrapper>.glyphicon-plus').click(function () {
        // 商品ID
        var goodsid = $(this).attr('goodsid')
        var $that = $(this) // 将this保存起来，因为在ajax请求中，this指向有问题

        // 发起ajax请求
        $.get('/axf/addtocart/', {'goodsid':goodsid}, function (response) {
            if (response['status'] == '-1'){    // 未登录
                // 跳转到登录界面
                window.open('/axf/login/', target="_self")
            } else {    // 已登录
                console.log(response)
                $that.prev().html(response['number']).show()
                $that.prev().prev().show()
            }
        })
    })


    // 减操作
    $('.bt-wrapper>.glyphicon-minus').click(function () {
        var goodsid = $(this).attr('goodsid')
        var $that = $(this)

        $.get('/axf/subtocart/', {'goodsid':goodsid}, function (response) {
            console.log(response)
            if (response['status'] == '1'){
                var number = parseInt(response['number'])
                if (number>0){  // 显示
                    $that.next().html(response['number'])
                } else {    // 隐藏
                    $that.next().hide()
                    $that.hide()
                }
            }
        })
    })
})