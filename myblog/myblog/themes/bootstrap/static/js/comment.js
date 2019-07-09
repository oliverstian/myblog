$(function () {

	// 未登录，下面都不执行，直接返回
	if($("#top-comment-area").has("h6").length>0){
        return;
	};

    //    点击回复
	$(".rep-btn").click(function(){
	    var i = $(this).data('repid')

		$(".cancel-btn").addClass("d-none"); //所有取消按钮都隐藏,以免在回复评论1时，点击评论2回复按钮，评论1仍显示取消
	    $(".rep-btn").removeClass("d-none");  //所有回复按钮都显示

		$(".rep-btn-all").addClass('d-none');  //先把所有回复框都隐藏
	    $('#rep-btn-'+i).removeClass('d-none');  //再把当前需要显示的回复框显示出来

		$(this).addClass('d-none');  //这两句为把回复按钮隐藏，显示取消按钮
		$(this).next(".cancel-btn").removeClass('d-none');
	});

	// 取消回复
	$(".cancel-btn").click(function () {
		var i = $(this).data('repid');

		$(this).addClass('d-none');  //点击后隐藏取消按钮
		$(this).prev(".rep-btn").removeClass('d-none');  //同时把回复按钮显示出来

		$('#rep-btn-'+i).children("textarea").val("");  //清空对应评论框的内容
		$('#rep-btn-'+i).addClass("d-none");  //随后把评论框隐藏
    })

	//提交评论
	$(".all-rep-comment-btn").click(function () {
        var comment_content = $(this).parent("div").prev("textarea").val();

        if (comment_content.length == 0) {
            alert("评论内容不能为空！");
            return;
        }

        var base_t = sessionStorage.getItem('base_t');
        var now_t = Date.parse(new Date());
        if (base_t) {
            var tt = now_t - base_t;
            if (tt < 10000) {
                alert('两次评论时间间隔必须大于10秒，还需等待' + (10 - parseInt(tt / 1000)) + '秒');
                return;
            } else {
                sessionStorage.setItem('base_t', now_t);
            }
        } else {
            sessionStorage.setItem('base_t', now_t)
        }
        ;

        var articleid = $(this).data("article-id");
        var reptoid = $(this).data("repto-id");
        var csrftocken = $(this).data("csrf");
        var url = $(this).data("ajax-url");

        $.ajaxSetup({
            data: {
                'csrfmiddlewaretoken': csrftocken
            }
        });


        $.ajax({
            type: "POST",
            url: url,
            data: {
                "article_id": articleid,
                "rep_id": reptoid,
                "content": comment_content
            },
            dataType: 'json',
            success: function (ret) {
                sessionStorage.setItem("new_point", ret.new_point);
                window.location.reload();
            },
            error: function (ret) {
                alert(ret.msg);
            }
        });
    });

	//    提交评论后定位到新评论处
    if(sessionStorage.getItem('new_point')){
        var top = $(sessionStorage.getItem('new_point')).offset().top-120;
        $('body,html').animate({scrollTop:top}, 500);
        window.location.hash = sessionStorage.getItem('new_point');
        sessionStorage.removeItem('new_point');
    };
})