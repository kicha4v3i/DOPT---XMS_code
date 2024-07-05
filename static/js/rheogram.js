$(function() {
    $(document).on("click",".addrheogram_sections" , function() {
        var tabcount = $("#section-tab a.nav-link").length;
        var tab=tabcount-1
        var userenter_lastdepth=$('input[name="todepth'+tab+'"]').val();
        var fromdepth=$('#rheo_fromdepth').val();
        var todepth=$('#rheo_todepth').val();
        var new_depth=parseFloat(userenter_lastdepth);
        section_name=parseInt(new_depth)+'-'+parseInt(todepth)
        // alert(section_name)
        // alert(tabcount)
        // alert("userdepth"+userenter_lastdepth)
        // alert("todepth"+todepth)
        // alert(typeof(userenter_lastdepth))
        // alert(typeof(todepth))
        if(parseFloat(userenter_lastdepth)<parseFloat(todepth)){
          // alert("vvc");
          var tabhtml=''
          tabhtml +='<a class="nav-link" id="section'+tabcount+'-tab" data-toggle="pill" href="#section'+tabcount+'" role="tab" aria-controls="v-pills-home" aria-selected="true">'
          tabhtml +='<div class="row">'
          tabhtml +='<div class="col-md-2"><button type="button" name="remove" data-id='+tabcount+' class="rheogramremove-tab iconaction"><i class="fa fa-trash"></i></button></div>'
          tabhtml +='<div class="col-md-3"><input type="text" name="section" value='+section_name+' class="form-control"></div>'
          tabhtml +='<div class="col-md-3"><input type="text" name="from_depth'+tabcount+'" value='+new_depth+' class="form-control"></div>'
          tabhtml +='<div class="col-md-3"><input type="text" name="todepth'+tabcount+'" value='+todepth+' class="form-control"></div>'
          tabhtml +='</div></a>'
          $('div#section-tab').append(tabhtml)
         
          $.ajax({
              type: "GET",
              url:"/wells/muddata/getrheogramrpm",
              success: function(data) {
      
              var html='<input type="hidden" name="rheogram_sections" value=""><div class="tab-pane fade" id="section'+tabcount+'" role="tabpanel" aria-labelledby="section'+tabcount+'-tab"><table id="rheogram-table'+tabcount+'"><thead><tr><th>RPM</th><th>Dial</th></tr></thead><tbody>';
              for(var i=0;i<data.length;i++){
                html +='<input type="hidden" name="rheogram_id'+tabcount+'" value=""><tr><td><input type="text" name="rpm'+tabcount+'" class="form-control" value='+data[i].fields.rheogram_rpm+' placeholder="Rpm"></td><td><input type="text" name="dial'+tabcount+'" class="form-control" placeholder="Dial"></td><td><button type="button" name="add" class="addrheogram-row iconaction" data-id='+tabcount+'><i class="fa fa-plus"></i></button><button type="button" name="remove" class="rheogramremove-row iconaction" data-id='+tabcount+'><i class="fa fa-trash"></i></button></td></tr>';
              }
              html +='</tbody></table></div>';
              $('div#section-content').append(html);
              }
            });
        }
    });
});