/**
 * Created by fsm on 15/10/3.
 */
function check_model_del() {
    var se = confirm(
        "注意:" +
        "删除模块会直接删除模块相关联的所有数据，包括目录，确定需要删除该模块吗 ？"
    );
    if (se != true)
      return false;
}

function chekc_model_group() {

     var re = confirm(
         "注意："+
         " 主机组组不存在，请先定义主机组"
     )

    return false;

}
function model_del(){

    var re = confirm(
        "注意：你确定要删除应用到节点下面的模块吗？"
    )
    if (re != true)

        return false;

}

function checkIP(sIPAddress)
{

    var sIPAddress=sIPAddress
    var IPsplit;
    var re=/^(\d{1,3}\.){3}\d{1,3}\/(\d{1,3}\.){3}\d{1,3}$/gi;
    var chkflag=true;
    var ErrMsg="你输入的是一个非法的IP地址段！\nIP段为：:xxx.xxx.xxx.xxx/xxx.xxx.xxx.xxx（xxx为0-255)!"

    if(sIPAddress.search(re)==-1){
       chkflag=false;
    }else{
    IPsplit=sIPAddress.split("/");
    IPsplit=IPsplit[0]+"."+IPsplit[1]
    IPsplit=IPsplit.split(".");

    for(i=0;i<8;i++){
          if(IPsplit[i]>255){
             chkflag=false;
             break;
          }
    }
    }
    if(!chkflag)
         alert(ErrMsg);
         return chkflag
}

 function CheckAll(val) {
 $("input[name='chkJob']").each(function() {
 this.checked = val;
 });
 }

 function showFileName()
            {
                            var file = document.getElementById("W3Cfuns_FileList");
                            for(var i = 0, j = file.files.length; i < j; i++)
                            {
                                         alert(file.files[i].name);
                            }
            }

function beforeSubmit(form) {
    if (form.host_group.value == '') {
        alert('请选择主机组！');
        form.host_group.focus();
        return false;
    }
}