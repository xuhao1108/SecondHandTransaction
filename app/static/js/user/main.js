/**
 * @function 修改用户登录方式：验证码登录/密码登录
 * @param type {string} 登录方式：verification_code：验证码登录；password：密码登录
 * */
function login_tpye(type) {
    let disabled_class = 'btn btn-lg btn-secondary disabled';
    let abled_class = 'btn btn-lg btn-primary';
    // 密码登录
    if (type === 'password') {
        // 修改按钮状态
        $('#by_password').attr('class', disabled_class)
        $('#by_verfication_code').attr('class', abled_class)
        // 修改登录类型
        $('input[name="type"]').val(Constant['USER_PASSWORD_LOGIN'])
        // 显示控件
        $('#by_password_div').removeAttr('hidden')
        $('#by_verification_code_div').attr('hidden', 'true')
        // 必填属性
        $('#password').attr('required', 'required')
        $('#verification_code').removeAttr('required')
    }
    // 验证码登录
    else {
        // 修改按钮状态
        $('#by_password').attr('class', abled_class)
        $('#by_verfication_code').attr('class', disabled_class)
        // 修改登录类型
        $('input[name="type"]').val(Constant['USER_CODE_LOGIN'])
        // 显示控件
        $('#by_password_div').attr('hidden', 'true')
        $('#by_verification_code_div').removeAttr('hidden', '')
        // 必填属性
        $('#password').removeAttr('required')
        $('#verification_code').attr('required', 'required')
    }
}

/**
 * @function 检查邮箱控件输入正确性
 * @param value {string} 邮箱控件输入值
 * */
function check_email(value) {
    // 提示框
    let obj = $('#alert_div')
    let reg = /^[0-9a-zA-Z_.-]+[@][0-9a-zA-Z_.-]+([.][a-zA-Z]+){1,2}$/;
    if (reg.test(value)) {
        obj.css('display', 'none')
        obj.text('')
        return true
    } else {
        obj.css('display', 'block')
        obj.text('请输入格式正确的邮件，例如：email@example.com')
        return false
    }
}

/**
 * @function 检查密码控件输入正确性
 * @param password {string} 密码控件输入值
 * @param password2 {string} 确认密码控件输入值
 * */
function check_password(password, password2) {
    // 提示框
    let obj = $('#alert_div')
    // 提示文本
    let info = ''
    // 正则表达式
    let reg = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{8,}$/
    if (password != password2) {
        info = '两次密码输入不一致，请重新输入！'
    } else if (password.length < 8) {
        info = '密码长度最少8位，请重新输入！'
    } else if (password.length > 16) {
        info = '密码长度最多16位，请重新输入！'
    } else if (!reg.test(password)) {
        info = '密码必须同时包含【大写字母，小写字母，数字，特殊符号】其中的两种类型！'
    } else {
        obj.css('display', 'none')
        obj.text(info)
        return true
    }
    obj.css('display', 'block')
    obj.text(info)
    return false
}

/**
 * @function 异步发送邮件验证码请求
 * @param url {string} 发送邮件验证码的链接
 * @param email {string} 用户邮箱
 * @param csrf_token {string} token
 * @param type {string} 发送类型
 * @param mode {string} 发送模型
 * @param endpoint {string} 模型端点,当mode为token时，需要端点链接和token拼接成完整的url
 * @param expire_time {int} 验证有效时间
 * @param reset_btn {boolean} 发送成功后是否重置发送按钮
 * */
function send_verification_code(url, email = '', csrf_token = '', type = '',
                                mode = '', endpoint = '', expire_time = 0, reset_btn = true) {
    // 表单输入值
    email = email ? email : $('#email').val()
    type = type ? type : $('input[name="type"]').val()
    let data = {
        'email': email,
        'csrf_token': csrf_token ? csrf_token : $('input[name="csrf_token"]').val(),
        'type': type
    }
    if (endpoint) {
        data['endpoint'] = endpoint
    }
    if (mode) {
        data['mode'] = mode
    }
    if (expire_time) {
        data['expire_time'] = expire_time
    }
    // 检查邮件输入正确性
    if (!check_email(email)) {
        alert('请检查邮件输入正确性');
        return false;
    }
    // 异步发送请求
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        success: function (data) {
            // 成功发送
            if (data['code'] == Constant['SUCCESS']) {
                // 修改按钮状态
                if (reset_btn) {
                    let wait_time = Constant['CODE_EXPIRE_TIME'];
                    // 注册验证码有效期更长
                    if (type == Constant['USER_REGISTER']) {
                        wait_time = Constant['CODE_EXPIRE_TIME'] * 5
                    }
                    set_wait_text($('#get_verification_code'), wait_time)
                }
                return true;
            }
            //已经发送过验证码
            else {
                alert(data['message']);
                //用户已存在
                if (data['code'] == Constant['USER_EXIST']) {
                    window.location.href = '/user/login';
                }
                //用户不存在
                else if (data['code'] == Constant['USER_NOT_EXIST']) {
                    window.location.href = '/user/register';
                }
                return false;
            }
        }
    })
}

/**
 * @function 修改发送邮件后按钮状态
 * @param obj {object} 按钮对象
 * @param wait_time {int} 等待时间
 * */
function set_wait_text(obj, wait_time) {
    let $this = $(obj);
    if (wait_time) {
        // 修改按钮为不可用状态
        $this.css('pointer-events', 'none');
        $this.css('background', '#999999');
        $this.css('color', '#FFFFFF');
        $this.html('重新发送(' + wait_time + ')');
        // 递归调用
        wait_time--;
        setTimeout(function () {
            set_wait_text(obj, wait_time)
        }, 1000)
    } else {
        // 修改按钮为可用状态
        $this.css('pointer-events', '');
        $this.css('background', '#549ff2');
        $this.html('发送验证码');
    }
}

/**
 * @function 个人空间界面‘修改密码’按钮点击事件
 * @param url {string} 修改密码链接
 * @param email {string} 邮箱
 * @param csrf_token {string} token
 * */
function reset_password(url, email, csrf_token) {
    // 弹出确认框
    let result = confirm('是否确定修改密码')
    if (!result) {
        return false;
    }
    // 异步发送邮件
    let send_reslut = send_verification_code(url, email, csrf_token, Constant['USER_RESET_PASSWORD'],
        Constant['TOKEN'], 'user.reset_password', 0, false)
    // 发送成功
    if (send_reslut) {
        alert('验证码发送成功，请注意查收！');
    }
}

/**
 * @function 预览用户选择修改的头像
 * @param input {object} 文件控件对象
 * */
function show_portrait(input) {
    let img_src = getObjectURL(input.files[0])
    $('#portrait_img').attr('src', img_src);
}

/**
 * @function 获取文件对象链接
 * @param file {object} 文件对象
 * */
function getObjectURL(file) {
    let url = null;
    if (window.createObjectURL != undefined) {
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}