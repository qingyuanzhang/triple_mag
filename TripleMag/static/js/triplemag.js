function test(){
    //alert($("select:eq(1)").val())
    $("#id_province").val($("select:eq(0)").val())
    $("#id_city").val($("select:eq(1)").val())
    $("#id_area").val($("select:eq(2)").val())
    //alert($("#id_area").val())
}
function cancle(){
    $("#add_address").fadeOut()
}
