$(function(){
    $('#profile_picture').change( function(e) {

        var img = URL.createObjectURL(e.target.files[0]);
        $('.prof_pic').attr('src', img);

    });

    $('#file-upload').change( function(e) {
        document.getElementById("import-form").submit();
    });

  });