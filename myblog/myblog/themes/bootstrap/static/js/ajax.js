function ajax(obj){
    // 1.创建XMLHtttpRequest对象(ajax对象)
    if (window.XMLHttpRequest) {
        var xhr = new XMLHttpRequest();
    } else {
        var xhr = new ActiveXObject('Microsoft.XMLHTTP');// code for ie5 ie6
    }

    if (obj.type == 'get' || obj.type == 'GET') {
        // 2.连接服务器
        xhr.open(obj.type,obj.url+'?'+obj.data+'&_='+new Date().getTime(),true);
        // 3.将请求发送到服务器
        xhr.send(null);//get请求
    } else if (obj.type == 'post' || obj.type == 'POST') {
        // 2.连接服务器
        xhr.open(obj.type,obj.url,true);
        // 设置http请求头
        xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        // 3.将请求发送到服务器
        xhr.send(obj.data);//post请求
    }

    // 4.等待服务器响应
    xhr.onreadystatechange = function (){
        if (xhr.readyState == 4) {//请求已完成
            if (xhr.status == 200) {//OK 成功
                obj.success(xhr.responseText);
            } else{
                obj.failed(xhr.status);
            }
        }
    }
}
