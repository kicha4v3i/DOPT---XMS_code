$('.eye').click(function(){
    var current_element=$(this).attr('data-type')
    var currentType = $('#'+current_element).attr('type');
       
    if($(this).closest('span').find('i').hasClass('icon-eye-off')){
      $(this).closest('span').find('i').removeClass('icon-eye-off');
      $(this).closest('span').find('i').addClass('icon-eye');
              
    }else{
      $(this).closest('span').find('i').removeClass('icon-eye');
      $(this).closest('span').find('i').addClass('icon-eye-off');  
    }
    if (currentType === 'password') {
        $('#'+current_element).attr('type','text');
    }else{
        $('#'+current_element).attr('type','password');

    }

});

function  createSVGFromChart(chart,target,name = ''){
    let svgString = chart.getSVG();
    let parser = new DOMParser(); 
    let svgElem = parser.parseFromString(svgString, "image/svg+xml").documentElement;
    let s = new XMLSerializer().serializeToString(svgElem);
    let b64 = 'data:image/svg+xml;base64,';
    b64 += btoa(s);

    svgString2Image(b64, 800, 600, 'png', function (pngData) {
        img = pngData.replace('data:image/png;base64,', '');
        var data ={
            png:img,
            filename:name,
        }
        $.ajax({
        type: "POST",
        url: "/wells/muddata/chart_image",
        data: {
            csrfmiddlewaretoken: csrf,
            data:data
        },
        success: function(data){
            // alert(data);
        }
        });
    });
}
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
function svgString2Image(svgString, width, height, format, callback) {
    format = format ? format : 'png';
    var svgData = svgString

    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = width;
    canvas.height = height;
    var image = new Image();
    image.onload = function () { 
        context.clearRect(0, 0, width, height);
        context.drawImage(image, 0, 0, width, height);
        var pngData = canvas.toDataURL('image/' + format);
        callback(pngData);
    }; 
    image.src = svgData;
}