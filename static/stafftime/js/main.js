$(document).ready(function(){

  $('.datepicker').pickadate({
    selectMonths: true,
    selectYears: 100
  });

  $('.delete').on('click', function(){
    if( confirm('Вы действительно хотите удалить?')){
      return true;
    } else {
      return false;
    }
  });
});