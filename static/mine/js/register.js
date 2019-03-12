$(function () {
    $('.register').width(innerWidth)

    //邮箱认证
    $('#email input').blur(function () {
        var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$")
        if ($(this).val() == ''){

            return}
        if (reg.test($(this).val())){
            request_data = {
                'email':$(this).val()
            }
            //调用ajax对接服务器进行验证
            $.get('/axf/checkemail/',request_data,function (response) {

                if(response.status){
                    $('#email-t').attr('data-content','恭喜你的帐号可用').popover('hide')
                    $('#email').removeClass('has-error').addClass('has-success')
                    $('#email>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
                }
                else{
                     $('#email-t').attr('data-content',response.msg).popover('show')
                    $('#email').removeClass('has-success').addClass('has-error')
                    $('#email>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
                }
            })
        }
        else {

            $('#email-t').attr('data-content','数据格式不正确 ').popover('show')
            $('#email').removeClass('has-success').addClass('has-error')
            $('#email>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    //密码认证
    $('#password input').blur(function () {
        var reg = new RegExp("^[a-zA-Z0-9_]{6,10}$")
        if ($(this).val() == '')    return
        if (reg.test($(this).val())){
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }else {
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })
    //确认密码
    $('#password-d input').blur(function () {

        if ($(this).val() == '')    return

        var f_val = $('#password input').val()
        var d_val = $('#password-d input').val()


        if (f_val == d_val){
            $('#password-t').popover('hide')
            $('#password-d').removeClass('has-error').addClass('has-success')
            $('#password-d>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }else {
            $('#password-t').popover('show')
            $('#password-d').removeClass('has-success').addClass('has-error')
            $('#password-d>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })
    //验证昵称
    $('#name input').blur(function () {
        if ($(this).val() == '') return
        if ($(this).val().length>=3 && $(this).val().length<=10) {
            $('#name').removeClass('has-error').addClass('has-success')
            $('#name>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }
        else {
            $('#name').removeClass('has-success').addClass('has-error')
            $('#name>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')

        }
    })

    //注册按钮
    $('#subButton').click(function () {

        var isregister = true
        $('.register .form-group').each(function () {
            if(!$(this).is('.has-success')){
                isregister = false
            }
        })
        if (isregister){
            $('.register form').submit()
            console.log('注册')
        }
    })

})