/**
 * @function 检查数字控件输入正确性：1~12位
 * @param obj {object} 数字 控件对象
 * */
function format_number(obj) {
    let value = obj.value.match(/[1-9]\d{0,11}(\.\d{1,2})?/g);
    if (value) {
        obj.value = value[0]
    } else {
        obj.value = ''
    }
}

/**
 * @function 检查百分比控件输入正确性：1~100
 * @param obj {object} 百分比 控件对象
 * */
function format_number_percent(obj) {
    let value = obj.value.match(/100|[1-9]\d/g);
    if (value) {
        obj.value = value[0]
    } else {
        obj.value = 1
    }
}

/**
 * @function 上传文件数量检测
 * @param obj {object} 百分比 控件对象
 * @param min {int} 文件数量下限
 * @param max {int} 文件数量上限
 * */
function check_file_count(obj, min = 1, max = 9) {
    if (window.File && window.FileList) {
        let count = obj.files.length;
        // 删除预览的图片
        $('#show_pictures').empty();
        if (count < min || count > max) {
            alert('文件数不能小于' + min + '个，也不能超过' + max + '个，而你选择了' + count + '个！');
            // 清空文件域
            let file = $('#pictures');
            file.after(file.clone().val(''));
            file.remove();
            return false;
        } else {
            // 预览图片
            show_pictures(obj)
            return true;
        }
    } else {
        alert('抱歉，你的浏览器不支持FileAPI，请升级浏览器！');
        return false;
    }
}

/**
 * @function 显示选择的图片预览图
 * @param obj {object} 文件对象
 * */
function show_pictures(obj) {
    // ul对象
    let ul = $('#show_pictures');
    for (let index = 0; index < obj.files.length; index++) {
        // 创建li对象
        let li = document.createElement('li');
        li.setAttribute('class', 'list-group-item');
        // 创建图片对象
        let img = document.createElement('img');
        img.setAttribute('width', '100px');
        img.setAttribute('height', '100px');
        // 获取图片临时链接
        let img_src = getObjectURL(obj.files[index])
        img.setAttribute('src', img_src);
        img.setAttribute('alt', obj.files[index].name);
        // 插入dom
        li.appendChild(img);
        ul.append(li);
    }
}

/**
 * @function 设置排序节点属性
 * @param obj {object} 排序节点对象
 * */
function set_sort_dom(obj) {
    let url = window.location.href
    let sort_key = '_' + obj.getAttribute('id');
    let sort_value = obj.getAttribute('sort');
    // 查找链接终的参数值
    let url_arg = get_url_arg(url, sort_key)
    if (url_arg) {
        sort_value = url_arg * -1
    } else {
        // 有默认值
        if (sort_value) {
            sort_value *= -1
        } else {
            sort_value = -1
        }
    }
    obj.setAttribute('sort', sort_value)
    // 设置元素的跳转页面
    obj.href = update_url_arg(url, sort_key, sort_value)
    // 设置元素排序图标
    let dom_i = document.createElement('i')
    // 当前为升序
    if (sort_value == 1) {
        // 设置图标为向下
        dom_i.setAttribute('class', 'bi bi-arrow-down')
    } else {
        // 设置图标为向上
        dom_i.setAttribute('class', 'bi bi-arrow-up')
    }
    obj.appendChild(dom_i)
}

/**
 * @function 修改链接参数值并返回新链接
 * @param url {string} 链接
 * @param arg {string} 需要替换的参数名
 * @param value {string} 需要替换的参数值
 * */
function update_url_arg(url, arg, value) {
    let replace_text = arg + '=' + value;
    // 原链接有当前参数
    if (get_url_arg(url, arg) != null) {
        let partten = new RegExp("(^|)" + arg + "=([^&]*)(|$)", 'i');
        console.log(partten)
        return url.replace(partten, replace_text)
    } else {
        if (url.match('[\?]')) {
            return url + '&' + replace_text;
        } else {
            return url + '?' + replace_text;
        }
    }
}


/**
 * @function 获取链接指定参数的值
 * @param url {string} 链接
 * @param arg {string} 需要获取的参数名
 * */
function get_url_arg(url, arg) {
    let partten = new RegExp("(^|\\?|&)" + arg + "=([^&]*)(&|$)", 'i');
    let result = url.match(partten);
    if (result) {
        return result[2]
    } else {
        return null;
    }
}

$(document).ready(function () {
    $('#sort_div a').each(function () {
        set_sort_dom(this)
    })
});
