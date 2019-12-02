// var pictures = ["53_0.jpg", "75_0.jpg"];
// function changePicture() {
//  var curr_pic = document.getElementById("image").src;
//  var split = curr_pic.split("/images/");
//  var start = split[0];
//  var file = split[1];
//  console.log(file);
//  var curr_picture = pictures.indexOf(file);
//  var newfile = pictures[(curr_picture + 1)% pictures.length];
//  var new_pic = start + "/images/" + newfile;
//  console.log(new_pic);
//  document.getElementById("image").src = new_pic;
// }


function setPicture(image_data) {
    //console.log('setting picture...');
    document.getElementById("image").src = image_data;
}

function setText(text) {
    $("#image_text").text(text);
}

function setPhotoNegative(negative) {
    $("#image_negative").val(negative);
}

function get_data_by_idx()
{
    var idx = parseInt($("#curr_idx").text()) + 1;

    $.ajax({
        type: "GET",
        url: "/get_data_by_index",
        data: {'curr_idx': idx},
        success: function (data) {
            //alert(data);
            //console.log('got data...')
            setPicture(data['image_data']);
            setText(data['text']);
            setPhotoNegative(data['id']);
            $("#curr_idx").text(idx);
        },
        error: function(xhr, status, error) {
            console.log(error)
        }
    });

}