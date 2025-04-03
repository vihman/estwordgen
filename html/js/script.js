/*$(function() {
	$('input[type=button]').click(function(event) {
		event.preventDefault();
		$('.content').text('Laadib...');
    	$.post('main.py', 'how='+ $('input[name=how]:checked').val()+'&len='+$('#len').val(),
    			function(data) {
            dataLoaded(self, data);
          });
	});
	function dataLoaded(marker, data) {
		var answer = $.parseJSON(data);
		var contentElem = $('.content');
		contentElem.html('');
		$.each(answer, function(key, word) {
			var conteiner = $('<div>').addClass('word');
			conteiner.text(word)
			contentElem.append(conteiner);
		})
	}
});*/
/*document.addEventListener('DOMContentLoaded', function(){
    // your code goes here
}, false);
*/
window.addEventListener("load", (event) => {
	console.log("loaded" + this);
	document.forms[0].addEventListener("submit", (e) =>{
		e.preventDefault()
		console.log("submitted" + this)
		document.getElementById('content').textContent = "Laadib..."
		const params = JSON.stringify(Object.fromEntries(new FormData(e.target)))
		fetch("/", {method: 'POST', body: params})
		    .then(Result => Result.json())
			.then(string => {
				// TODO:
				console.log(string);
    })
    .catch(errorMsg => { console.log(errorMsg); });
	})
});
