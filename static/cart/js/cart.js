$(function () {
    $('.cart').width(innerWidth)

    // 总计
    total()

    // 商品 选中 状态
    $('.cart .confirm-wrapper').click(function () {
        var cartid = $(this).attr('cartid')
        var $that = $(this)

        $.get('/axf/changecartstatus/', {'cartid':cartid}, function (response) {
            console.log(response)
            if (response['status'] == '1'){
                var isselect = response['isselect']
                $that.attr('isselect', isselect)
                // 先清空
                $that.children().remove()
                if (isselect){  // 选中
                    $that.append('<span class="glyphicon glyphicon-ok"></span>')
                } else {    // 未选中
                    $that.append('<span class="no"></span>')
                }

                // 总计
                total()
            }
        })
    })

    // 全选/取消全选
    $('.cart .bill .all').click(function () {
        var isall = $(this).attr('isall')
        isall = (isall == 'false') ? true : false
        $(this).attr('isall', isall)

        // 自身状态
        $(this).children().remove()
        if (isall){ // 全选
            $(this).append('<span class="glyphicon glyphicon-ok"></span>').append('<b>全选</b>')
        } else {    // 取消全选
            $(this).append('<span class="no"></span>').append('<b>全选</b>')
        }


        // 发起ajax请求
        $.get('/axf/changecartselect/', {'isall':isall}, function (response) {
            console.log(response)
            if (response['status'] == '1'){
                // 遍历
                $('.confirm-wrapper').each(function () {
                    $(this).attr('isselect', isall)
                    $(this).children().remove()
                    if (isall){ // 选中
                        $(this).append('<span class="glyphicon glyphicon-ok"></span>')
                    } else {    // 未选中
                        $(this).append('<span class="no"></span>')
                    }
                })

                // 总计
                total()
            }
        })
    })

    // 计算总数
    function total() {
        var sum = 0

        // 遍历
        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            // 选中，才计算
            if ($confirm.find('.glyphicon-ok').length){
                var price = parseInt($content.find('.price').attr('str'))
                var num = parseInt($content.find('.num').attr('str'))
                sum += num * price
            }
        })

        // 修改总计 显示
        $('.bill .total b').html(sum)
    }


    // 下单
    $('#generate-order').click(function () {
        $.get('/axf/generateorder/', function (response) {
            console.log(response)
            if (response['status'] == '1'){ // 订单详情(付款)
                var orderid = response['orderid']
                window.open('/axf/orderinfo/?orderid='+orderid, target='_self')
            }
        })
    })
})