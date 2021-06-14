/**
 * @function 依次显示类别的下拉菜单
 * @param level {int} 当前类别的层级
 * */
function show_catagory(level) {
    // 获取子节点个数，其中有一个为lebel标签
    let parent_dom = $('#catagory_div');
    let input = $('#catagory')
    let select_length = parent_dom.children().length - 1
    // 删除此层级后的所有节点
    for (let index = level; index <= select_length; index++) {
        $('#level_' + index).remove()
    }
    // 清空类别输入框
    input.val('');
    // 获取需要显示层级的上一级被选元素
    let select_value = $('#level_' + (level - 1) + ' option:selected').val()
    // 上一级被选元素为空，则表示是顶层元素，所以为0
    select_value = select_value ? select_value : 0
    let current_catagory = catagory[level - 1][select_value]
    let child = current_catagory['child']
    // 选择到最后一层，则将id添加到控件中
    if ($.isEmptyObject(child)) {
        input.val(current_catagory['item']['id']);
        return false;
    }
    // 创建select控件
    let dom_select = document.createElement('select');
    // 设置属性：id，class，onchange
    dom_select.setAttribute('id', 'level_' + (level))
    dom_select.setAttribute('class', 'custom-select my-1 mr-sm-2')
    dom_select.setAttribute('onchange', 'show_catagory(' + (level + 1) + ')')
    // 设置第一项为空
    let dom_option = document.createElement('option');
    // 设置不可选
    dom_option.setAttribute('style', 'display: none')
    // 将option控件添加到select中
    dom_select.appendChild(dom_option)
    for (let index in child) {
        // 创建option控件
        let dom_option = document.createElement('option');
        // 设置属性：value，innerHTML
        dom_option.setAttribute('value', child[index]['item']['id'])
        dom_option.innerHTML = child[index]['item']['name']
        // 将option控件添加到select中
        dom_select.appendChild(dom_option)
    }
    // 将select控件添加到div中
    parent_dom.append(dom_select)
}

/**
 * @function 根据类别控件id，自动选择类别下拉菜单
 * */
function select_catagory() {
    // 控件值
    let input_value = parseInt($('#catagory').val())
    // 默认显示第一层级，默认值是修改前的值
    show_catagory(1)
    // 保存从父到子的所有id
    let parent_list = [input_value]
    let current_level = Object.keys(catagory).length - 1
    // 找到当前层级
    for (let level = current_level; level >=0; level--) {
        if ($.inArray(input_value,catagory[level])){
            current_level = level;
            break;
        }
    }
    // 找到当前类别的所有父id
    find_catagory_parent(current_level, input_value, parent_list)
    // 反转数组，从父到子
    parent_list.reverse()
    // 按照等级，根据类别id选取对应的类别
    for (let level = 1; level <= parent_list.length; level++) {
        // 设置选中
        $('#level_' + level).find('option[value="' + parent_list[level - 1] + '"]').attr('selected', true);
        // 显示下一层级
        show_catagory(level + 1)

    }
}


/**
 * @function 递归查找当前类别的父id
 * @param level {int} 当前层级
 * @param c_id {int} 当前类别的id
 * @param result {Array} 保存从父到子的所有类别id
 * */
function find_catagory_parent(level, c_id, result) {
    if (c_id) {
        // 获取当前层级选择的元素
        let p_id = catagory[level][c_id]['parent_id'];
        if (p_id) {
            // 将父id添加到列表中
            result.push(p_id)
            // 寻找父id的父id
            find_catagory_parent(level - 1, p_id, result)
        }
    }
}