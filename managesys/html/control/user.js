$(document).ready(function() {
    $('#userDt').DataTable({
        "searching": false,
        "bPaginate": false,
        "bInfo": false, //是否显示页脚信息，DataTables插件左下角显示记录数  
        "bLengthChange": false, //去掉每页显示多少条数据方法
        "language": {
            url: 'html/chinese.json'
        },
        "columns": [{
            width: '40px',
            data: function() {
                return "<div class='ui fitted slider checkbox'>" +
                    "<input type='checkbox' id='this.name' onclick= 'checkbox_click(this)'> <label></label> </div>"
            }
        }, {
            //序号
            width: '40px',
            data: function(row, type, set, meta) {
                var c = meta.settings._iDisplayStart + meta.row + 1;
                return c;
            }
        }, {
            "data": "name"
        }, {
            "data": "email"
        }, {
            "data": "password"
        }, {
            "data": "create_time"
        }],
        "ajax": "/users"
    });
    $("#btn_all_del").api({
        url: '/users',
        method: 'DELETE',
        beforeXHR: (xhr) => {

            xhr.setRequestHeader('Content-Type', 'application/json');

        },
        beforeSend: (settings) => {
            var checkeds = $('input:checkbox:checked');
            settings.data = JSON.stringify({
                "datas": ["1", "2", "4"],
                "name": "zyf"
            });
            return settings;
        },
        onSuccess: function(response) {
            console.log(response);
        }
    });
    /**
     * easyui
     */
    //动态加载标题和数据
    $.ajax({
        url: "/users",
        type: "get",
        dataType: "json",
        success: function(data) {
            $("#dg").datagrid("loadData", data.data); //动态取数据
        }
    });
    $('#dg').datagrid({
        columns: [
            [{
                field: 'name',
                title: '姓名',
            }, {
                field: 'email',
                title: 'Email',
            }, {
                field: 'password',
                title: '密码',
            }, {
                field: 'create_time',
                title: '创建时间',
            }]
        ]
    });
})


function checkbox_click(checkbox) {
    if (checkbox.checked) {
        var btn_del = $("#btn_del");
        btn_del.removeClass("disabled");
        //btn_del.addClass("ui small button");
    } else {
        var btn_del = $("#btn_del");
        //btn_del.removeClass();
        btn_del.addClass("disabled");
    }
}
var url;

function newUser() {
    $('#dlg').dialog('open').dialog('center').dialog('setTitle', '增加用户');
    $('#fm').form('clear');
    url = '/users';
}

function editUser() {
    var row = $('#dg').datagrid('getSelected');
    if (row) {
        $('#dlg').dialog('open').dialog('center').dialog('setTitle', '编辑用户');
        $('#fm').form('load', row);
        url = 'update_user.php?id=' + row.id;
    }
}

function saveUser() {
    $('#fm').form('submit', {
        url: url,
        onSubmit: function() {
            return $(this).form('validate');
        },
        success: function(result) {
            $.messager.alert('Info', result, 'info');
        }
    });
}

function destroyUser() {
    var row = $('#dg').datagrid('getSelected');
    if (row) {
        $.messager.confirm('确定', '是否要删除所选用户?', function(r) {
            if (r) {
                $.post('destroy_user.php', { id: row.id }, function(result) {
                    if (result.success) {
                        $('#dg').datagrid('reload'); // reload the user data
                    } else {
                        $.messager.show({ // show error message
                            title: 'Error',
                            msg: result.errorMsg
                        });
                    }
                }, 'json');
            }
        });
    }
}