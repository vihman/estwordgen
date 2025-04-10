window.addEventListener("load", (event) => {
	console.log("loaded" + this);
	document.forms[0].addEventListener("submit", (e) =>{
		e.preventDefault()
		console.log("submitted" + this)
		const content = document.getElementById('content')
		content.textContent = "Laadib..."
		var params = Object.fromEntries(new FormData(e.target))
		params.len = parseInt(params.len);
		params = JSON.stringify(params)
		fetch("https://08k9fou89e.execute-api.eu-north-1.amazonaws.com/default/api/", {method: 'PUT', body: params})
		    .then(Result => Result.json())
			.then(results => {
				//words = JSON.parse(results)
				const b = JSON.parse(JSON.parse('"' + results.body.replace(/\"/g, '\\"') + '"'))
				content.textContent = ""
				b.forEach( function(elem, index, arr) {
					const p = document.createElement("div")
					p.textContent = elem
					content.appendChild(p)
				})
    })
    .catch(errorMsg => { console.log(errorMsg); });
	})
});
