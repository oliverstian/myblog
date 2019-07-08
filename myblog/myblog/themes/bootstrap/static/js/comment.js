$(function () {

    //    点击回复
	$(".rep-btn").click(function(){
	    var u = $(this).data('repuser')
	    var i = $(this).data('repid')

		$(".comment-btn-all").addClass('d-none')
	    $('#comment-btn-'+i).removeClass('d-none')
		// $("#no-rep").removeClass('hidden');
		// $(".rep-btn").css("color", "#868e96");
		// $(this).css("color", "red");
		// $('html, body').animate({
		// 	scrollTop: $($.attr(this, 'href')).offset().top - 55
		// }, 500);
	});


















})