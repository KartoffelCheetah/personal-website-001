// OVERFLOW
function Overflowed(element){
	/***
	**  returns if width is less than scrollWidth
	**  I added a 10pixel difference just to be sure
	***/
	return element.innerWidth() < element[0].scrollWidth - 10 ? true : false;
}
function toggleOverflow(element){
	/***
	**  Toggles visibility between mobile and widescreen element.
	***/
	switch (Overflowed(element)) {
		case true: element.addClass('overflowed');break;
		default: element.removeClass('overflowed');break;
	}
}
// SELECT
function cutUrl (url) {
	/***
	**  returned url does not contain
	**  port, search, hash
	***/
	return url.protocol+'//'+url.hostname+url.pathname;
}
function markCurrentUrl(){
	// Add .selected class to urls leading to current page.
	$('a[href]').each(function(){
		var hyperlinkURL = new URL(this.href, window.location);
		if (cutUrl(hyperlinkURL) === cutUrl(window.location)) {
			$(this).addClass('selected');
		}
	});
}
