jQuery(function ($) {
	'use strict',

	//Countdown js
	$("#countdown").countdown({
			date: "10 july 2017 12:00:00",
			format: "on"
		},

		function () {
			// callback function
		});



	//Scroll Menu

	function menuToggle() {
		var windowWidth = $(window).width();

		if (windowWidth > 767) {
			$(window).on('scroll', function () {
				if ($(window).scrollTop() > 405) {
					$('.main-nav').addClass('fixed-menu animated slideInDown');
				} else {
					$('.main-nav').removeClass('fixed-menu animated slideInDown');
				}
			});
		} else {

			$('.main-nav').addClass('fixed-menu animated slideInDown');

		}
	}

	menuToggle();


	// Carousel Auto Slide Off
	$('#event-carousel, #twitter-feed, #sponsor-carousel ').carousel({
		interval: false
	});


	// Contact form validation
	var form = $('.contact-form');
	form.submit(function () {
		'use strict',
		$this = $(this);
		$.post($(this).attr('action'), function (data) {
			$this.prev().text(data.message).fadeIn().delay(3000).fadeOut();
		}, 'json');
		return false;
	});

	$(window).resize(function () {
		menuToggle();
	});

	$('.main-nav ul').onePageNav({
		currentClass: 'active',
		changeHash: false,
		scrollSpeed: 900,
		scrollOffset: 0,
		scrollThreshold: 0.3,
		filter: ':not(.no-scroll)'
	});

});

$("#upload").click(function getContact() {
	try

	{

		jQuery.support.cors = true;

		$.ajax({
			type: "get",
			url: "/sendmail",
			data: {
				name:$("#name").val(),
				email:$("#email").val(),
				message:$("#message").val()
			},
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			cache: false,
			processData: true,
			success: function (response) {
				// do something
				alert("El mensaje se ha enviado: " + response);
			},

			error: function (error) {
				// error handler
				alert("Error enviando el mail")
			}

		});

	} catch (error) {
		alert(error);
	}

});