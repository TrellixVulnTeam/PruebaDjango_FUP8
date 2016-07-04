function buscarProv(val) {

		$.ajax({
			type: "POST",
			url: '/buscarProv/',
			data: {
				'dept' : val,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: function (response) {
       		document.getElementById("provinces_list1").innerHTML=response; 
    		}
		});
};

function buscarDist(val) {

		$.ajax({
			type: "POST",
			url: '/buscarDist/',
			data: {
				'dpt' : val,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: function (response) {
       		document.getElementById("districts_list1").innerHTML=response; 
    		}
		});
};

function buscarProv2(val) {

		$.ajax({
			type: "POST",
			url: '/buscarProv/',
			data: {
				'dept' : val,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: function (response) {
       		document.getElementById("provinces_list2").innerHTML=response; 
    		}
		});
};

function buscarDist2(val) {

		$.ajax({
			type: "POST",
			url: '/buscarDist/',
			data: {
				'dpt' : val,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: function (response) {
       		document.getElementById("districts_list2").innerHTML=response; 
    		}
		});
};

function listarItem(val) {

		$.ajax({
			type: "GET",
			url: '/listarItem/'+val+'/',
			data: {
				
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: function (response) {
       		document.getElementById(val).innerHTML=response; 
    		}
		});
};

function contarEvidencia(conv_conv,caract) {

    $.ajax({
      type: "POST",
      url: '/contarEvidencia/',
      data: {
        'conv_conv' : conv_conv,
        'caract' : caract,
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
          document.getElementById("e"+caract).innerHTML=response; 
        }
    });
};
  
function puntajeCaracteristica(conv_conv,caract) {

    $.ajax({
      type: "POST",
      url: '/puntajeCaracteristica/',
      data: {
        'conv_conv' : conv_conv,
        'caract' : caract,
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
          document.getElementById("p"+caract).innerHTML=response; 
        }
    });
};

function valorMaxCaracteristica(conv_conv,caract) {

    $.ajax({
      type: "POST",
      url: '/valorMaxCaracteristica/',
      data: {
        'conv_conv' : conv_conv,
        'caract' : caract,
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
          document.getElementById("vm"+caract).innerHTML=response; 
        }
    });
};