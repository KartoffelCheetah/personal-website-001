// FULLSCREEN
$(function getFullscreen(){
	// toggles between display or hide modal
	// https://davidwalsh.name/fullscreen
	var
		modal100 = $('.non-touch #modal100'),
		theImage = $('.non-touch #TheImage')
	;
	modal100.find('img').prop('title', 'Click to change the View');
	theImage.find('img').prop('title', 'Click to change the View');
	theImage.click(function(){
		modal100.removeClass('hidden');
		// modal100van['requestFullscreen'] = modal100van.requestFullscreen || modal100van.mozRequestFullScreen || modal100van.webkitRequestFullscreen || modal100van.msRequestFullscreen;
		// if (modal100van.requestFullscreen) modal100van.requestFullscreen();
	})
	modal100.click(function(){
		modal100.addClass('hidden');
		// document['exitFullscreen'] = document.exitFullscreen || document.mozCancelFullScreen || document.webkitExitFullscreen || document.msExitFullscreen;
		// if (document.exitFullscreen) document.exitFullscreen();
	})
})
// OVERFLOW SLIDER
$(function sliderOverflow(){
	// adding .overflowed class to element
	var /*global variable for toggleOverflow*/
		photoSlider = $('.photo-slider')
	;

	$(toggleOverflow.bind(window, photoSlider)); //on ready
	$(window).resize(toggleOverflow.bind(window, photoSlider)); //on resize
})
