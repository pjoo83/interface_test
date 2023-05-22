function msg_info(txt){
    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.info);
}
function msg_note(txt){
    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.confirm);
}
function msg_warn(txt){
    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.warning);
}
function msg_error(txt){
    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.error);
}
function msg_success(txt){
    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.success);
}
function msg_input(txt){
    var txt=  "请输入";
    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.input,{
        onOk:function(v){
            console.log(v);
        }
    });
}
function msg_auto(txt){
    var option = {
        title: "自定义标题",
        btn: parseInt("0011",2),
        onOk: function(){
            console.log("确认啦");
        }
    }
    window.wxc.xcConfirm(txt, "custom", option);
}
function msg_def(txt){
    window.wxc.xcConfirm(txt);
}









