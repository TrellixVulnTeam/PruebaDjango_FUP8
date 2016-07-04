var ubigeoPeru = {
	ubigeos: new Array()
};

document.addEventListener('DOMContentLoaded', function() {
	var request = new XMLHttpRequest;
	request.open('GET', 'static/ubigeo-peru.json', true);
	request.onload = onLoad_Request;
	request.send();

	function onLoad_Request() {
		if (request.status >= 200 && request.status < 400) {
			ubigeoPeru.ubigeos = JSON.parse(request.responseText);

			showRegionsList();
		}
	}
});

function showRegionsList() {
	var select = document.createElement('select');
	ubigeoPeru.ubigeos.forEach(function(ubigeo) {
		if (ubigeo.codprov === '00' && ubigeo.coddist === '00') {
			var option = document.createElement('option');

			var input = document.createElement('input');
			input.id = 'dpto-' + ubigeo.coddpto;
			input.name = 'coddpto';
			input.type = 'text';
			input.value = ubigeo.coddpto;
			select.onchange = onChange_Region(this.value);
			//input.addEventListener('change', onChange_Region(input.value), false);

			var label = document.createElement('label');
			label.htmlFor = 'dpto-' + ubigeo.coddpto;
			label.textContent = ubigeo.coddpto + ' ' + ubigeo.codprov + ' ' + ubigeo.coddist + ' - ' + ubigeo.nombre;

			option.appendChild(input);
			option.appendChild(label);

			document.querySelector('#regions-list').appendChild(option);
			//console.log(input.addEventListener('change', onChange_Region, false))
		}
	});
}

function onChange_Region(valor) {
	document.querySelector('#provinces-list').innerHTML = '';
	document.querySelector('#districts-list').innerHTML = '';

	showProvincesList(valor);
	console.log("alexlo27"+this.value)
}

function showProvincesList(coddpto) {
	ubigeoPeru.ubigeos.forEach(function(ubigeo) {
		if (ubigeo.coddpto === coddpto && ubigeo.codprov !== '00' && ubigeo.coddist === '00') {
			var option = document.createElement('option');

			var input = document.createElement('input');
			input.id = 'prov-' + ubigeo.codprov;
			input.name = 'codprov';
			input.type = 'radio';
			input.value = ubigeo.codprov;
			input.addEventListener('change', onChange_Province, false);

			var label = document.createElement('label');
			label.htmlFor = 'prov-' + ubigeo.codprov;
			label.textContent = ubigeo.coddpto + ' ' + ubigeo.codprov + ' ' + ubigeo.coddist + ' - ' + ubigeo.nombre;

			option.appendChild(input);
			option.appendChild(label);

			document.querySelector('#provinces-list').appendChild(option);
		}
	});
}

function onChange_Province() {
	document.querySelector('#districts-list').innerHTML = '';

	var coddpto = document.querySelector('[name=coddpto]:checked').value;

	showDistrictsList(coddpto, this.value);
}

function showDistrictsList(coddpto, codprov) {
	ubigeoPeru.ubigeos.forEach(function(ubigeo) {
		if (ubigeo.coddpto === coddpto && ubigeo.codprov === codprov && ubigeo.coddist !== '00') {
			var option = document.createElement('option');

			var input = document.createElement('input');
			input.id = 'dist-' + ubigeo.coddist;
			input.name = 'coddist';
			input.type = 'radio';
			input.value = ubigeo.coddist;

			var label = document.createElement('label');
			label.htmlFor = 'dist-' + ubigeo.coddist;
			label.textContent = ubigeo.coddpto + ' ' + ubigeo.codprov + ' ' + ubigeo.coddist + ' - ' + ubigeo.nombre;

			option.appendChild(input);
			option.appendChild(label);

			document.querySelector('#districts-list').appendChild(option);
		}
	});
}