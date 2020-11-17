function onReady(callback) {
    var intervalID = window.setInterval(checkReady, 1);
    function checkReady() {
        if (document.getElementsByTagName('body')[0] !== undefined) {
            window.clearInterval(intervalID);
            callback.call(this);
        }
    }
}

function show(id, value) {
    document.getElementById(id).style.display = value ? 'block' : 'none';
}

onReady(function () {
    show('loading', false);
});

$(document).ready(function(){
  $("#search-input").on("keyup keypress", function(e) {
    var keyCode = e.keyCode || e.which;
    if(keyCode === 13) { 
        e.preventDefault();
        return false;
    }else{
        var value = $(this).val().toLowerCase();
        if(value.length > 2 || value.length < 1){
            $("#table-pessoas tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        }
    }
  });
  $(".loadme").on("click", function(e){
    show('loading', true);
  })

  $('select').select2();

  $('input[name^="data"]').each(function(){
    $(this).datepicker({format:'dd/mm/yyyy',});;
  });

});

