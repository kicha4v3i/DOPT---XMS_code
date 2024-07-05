var sensitivity={}
$('.popup-presstbl').DataTable();

$(document).ready(function() {
    var mudweight_pressure_chart
    var flowrate_pressure_chart
    var mudweightecd_chart
    var flowrateecd
    $(document).on("click", ".sensitivity" , function() {
        var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
        var section_name = $('ul.custom_active_list').find('li.active').attr('data-id'); 
        var flowrate=$('.flowrate').val();
        var rpm=$('.rpm').val();
        var rop=$('#rop_userenter').val();
        var cuttings_density=$('#cuttings_density').val()
        var cuttings_size=$('#cuttings_size').val()
        var mudweight=$('#mudweight_hidden').val()
        var plastic_viscocity=$('#pv_hidden').val()
        var yieldpoint=$('#yp_hidden').val()
        var bitdepth=$('#todepth_hidden').val()
        $('#flowrate_sensitivity').val(flowrate)
        $('#rop_sensitivity').val(rop)
        $('#cs_sensitivity').val(cuttings_size)
        $('#cd_sensitivity').val(cuttings_density)
        $('#mudweight_sensitivity').val(mudweight)
        $('#pv_sensitivity').val(plastic_viscocity)
        $('#yp_sensitivity').val(yieldpoint)
        flowrate_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        mudweight_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        tfa_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        viscocity_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        yieldpoint_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        rop_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        cd_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        cs_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        // createSVGFromChart(directchart_slip, 'pressurelosschart_canvas','directchart_slip-'+wellphase_id+'-'+section_name);
    })
    $(document).on("blur", ".sensitivity_input" , function() {
        var data_type=$(this).attr('data-type')
        var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
        var section_name = $('ul.custom_active_list').find('li.active').attr('data-id'); 
        var flowrate=$('#flowrate_sensitivity').val()
        var rpm=$('.rpm').val();
        var rop=$('#rop_sensitivity').val()
        var cuttings_density=$('#cd_sensitivity').val()
        var cuttings_size=$('#cs_sensitivity').val()
        var bitdepth=$('#todepth_hidden').val() 
        var mudweight=$('#mudweight_sensitivity').val()
        var plastic_viscocity=$('#pv_sensitivity').val()
        
        flowrate_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')
        mudweight_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')
        tfa_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')
        viscocity_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')
        yieldpoint_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','nochange')
        rop_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')
        cd_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')
        cs_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'original','changed')






        // switch(data_type){
        //     case 'flowrate':
        //         mudweight_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'changed','flowratechanged')
        //         break;
        //     case 'mudweight':
        //         flowrate_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'changed','mudweightchanged')
        //         break;
        //     case 'pv':
        //         flowrate_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,'changed','pvchanged')
        //         break;
        //     case 'yp':


        //     default:
        //         console.log("gg")
        // }
    })

    $(document).on("click",".mudweight_pressure_sensitivity",function(){
        $('.mudweight-pressure-modal').modal('show');
    });
    $(document).on("click",".tfa_pressure_sensitivity",function(){
        $('.tfa-pressure-modal').modal('show');
    });

    $(document).on("click",".yieldpoint_pressure_sensitivity",function(){
        $('.yieldpoint-pressure-modal').modal('show');
    });

    $(document).on("click",".flowrate_pressure_sensitivity",function(){
        $('.flowrate-pressure-modal').modal('show');
    });
    $(document).on("click",".plastic_viscocity_pressure_sensitivity",function(){
       
        $('.plastic_viscocity-pressure-modal').modal('show');
    });

    $(document).on("click",".flowrate_ecd_sensitivity",function(){
        $('.flowrate_ecd_sensitivity').modal('show');
    });

    $(document).on("click",".mudweight_ecd_sensitivity",function(){
        $('.mudweight_ecd_sensitivity').modal('show');
    });

    $(document).on("click",".rop_ecd_sensitivity",function(){
        $('.rop_ecd_sensitivity').modal('show');
    });

    $(document).on("click",".cutting_density_ecd_sensitivity",function(){
        $('.cd_ecd_sensitivity').modal('show');
    });

    $(document).on("click",".cutting_size_ecd_sensitivity",function(){
        $('.cs_ecd_sensitivity').modal('show');
    });
    $(document).on("click",".plastiv_viscocity_ecd_sensitivity",function(){
        $('.plastic_viscocity-ecd-modal').modal('show');
    });

     

     
    

     
 

    

     

})
function cs_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var download_url = $('#pressurelosschart-url').data('base-url');
    var cs_ecdwith_chart_url = download_url.replace('charttype', 'cs_ecdwith');
    var cs_ecdwith_chart_url = cs_ecdwith_chart_url.replace(0, wellphase_id);
    var yp = $('#yp_sensitivity').val()

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'cs_ecd',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
        $('#cuttingssize_ecd_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#cuttingssize_ecd_chart').css("text-align", "center");
        },
        success: function(data) {
            cuttingssizeecdchart(data)
            sensitivity['cuttingssizeecdchart']=data
        
            var cs_ecdwith_datatable="";
            cs_ecdwith_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Cuttings Size</h4></tr><tr><th>Cuttings size</th><th>ECD with</th><th>ECD without</th></tr></thead><tbody>";
            for(var i=0;i<data.ecd_with.length;i++){
                cs_ecdwith_datatable +='<tr><td>'+data.ecd_with[i].x+'</td><td>'+data.ecd_with[i].y+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            }
            cs_ecdwith_datatable +="</tbody></table></div>";
            cs_ecdwith_datatable +='<button class="ecd-button"><a href="' + cs_ecdwith_chart_url + '">Download <i class="fa fa-download icon-down"></a></button>';
            $('#cs_ecdwith_datatable').html(cs_ecdwith_datatable);

            // var cs_ecdwithout_datatable="";
            // cs_ecdwithout_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>Yield Point</h4></tr><tr><th>Yield Point</th><th>Pressure Loss</th></tr></thead><tbody>";
            // for(var i=0;i<data.ecd_without.length;i++){
            //     cs_ecdwithout_datatable +='<tr><td>'+data.ecd_without[i].x+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            // }
            // cs_ecdwithout_datatable +="</tbody></table></div>";
            // cs_ecdwithout_datatable +='<button><a href="' + cs_ecdwithout_chart_url + '">Download</a></button>';
            // $('#cs_ecdwithout_datatable').html(cs_ecdwithout_datatable);
        },
        complete: function(){
            $('#cuttingssize_ecd_chart').closest('div').find('.loading-gif').remove()
            createSVGFromChart(cuttingssize_ecd_chart, 'pressurelosschart_canvas','cuttings_size_ecd-'+wellphase_id+'-'+section_name);
        },
     
    });

}
function cd_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var download_url = $('#pressurelosschart-url').data('base-url');
    var cd_ecdwith_chart_url = download_url.replace('charttype', 'cd_ecdwith');
    var cd_ecdwith_chart_url = cd_ecdwith_chart_url.replace(0,wellphase_id);
    // var cd_ecdwithout_chart_url = download_url.replace('charttype', 'cd_ecdwith');
    var yp = $('#yp_sensitivity').val()

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'cd_ecd',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
        $('#cuttingsdensity_ecd_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#cuttingsdensity_ecd_chart').css("text-align", "center");
        },
        success: function(data) {
            cuttingsdensityecdchart(data)
            console.log('cd_data_all',data)
            console.log('cd_data_with',data.ecd_with)
            sensitivity['cuttingsdensityecdchart']=data

            var cd_ecdwith_datatable="";
            cd_ecdwith_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Cuttings Density</h4></tr><tr><th>Cuttings density</th><th>ECD with</th><th>ECD without</th></tr></thead><tbody>";
            for(var i=0;i<data.ecd_with.length;i++){
                cd_ecdwith_datatable +='<tr><td>'+data.ecd_with[i].x+'</td><td>'+data.ecd_with[i].y+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            }
            cd_ecdwith_datatable +="</tbody></table></div>";
            cd_ecdwith_datatable +='<button class="ecd-button"><a href="' + cd_ecdwith_chart_url + '">Download <i class="fa fa-download icon-down"></a></button>';
            $('#cd_ecdwith_datatable').html(cd_ecdwith_datatable);

            // var cd_ecdwithout_datatable="";
            // cd_ecdwithout_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>Yield Point</h4></tr><tr><th>Yield Point</th><th>Pressure Loss</th></tr></thead><tbody>";
            // for(var i=0;i<data.result.length;i++){
            //     cd_ecdwithout_datatable +='<tr><td>'+data.result[i].x+'</td><td>'+data.result[i].y+'</td></tr>';
            // }
            // cd_ecdwithout_datatable +="</tbody></table></div>";
            // cd_ecdwithout_datatable +='<button><a href="' + cd_ecdwithout_chart_url + '">Download</a></button>';
            // $('#cd_ecdwithout_datatable').html(cd_ecdwithout_datatable);
        },
        complete: function(){
            $('#cuttingsdensity_ecd_chart').closest('div').find('.loading-gif').remove()
            createSVGFromChart(cuttingsdensity_ecd_chart, 'pressurelosschart_canvas','cuttings_density_ecd-'+wellphase_id+'-'+section_name);
        },
     
    });

}
function rop_ecd_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var download_url = $('#pressurelosschart-url').data('base-url');
    var rop_ecdwith_chart_url = download_url.replace('charttype', 'rop_ecdwith');
    var rop_ecdwith_chart_url = rop_ecdwith_chart_url.replace(0, wellphase_id);
    var yp = $('#yp_sensitivity').val()

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'rop_ecd',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
        $('#rop_ecd_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#rop_ecd_chart').css("text-align", "center");
        },
        success: function(data) {
            ropecdchart(data)
            sensitivity['ropecdchart']=data

            var rop_ecdwith_datatable="";
            rop_ecdwith_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>ROP</h4></tr><tr><th>Rop</th><th>ECD with</th><th>ECD without</th></tr></thead><tbody>";
            for(var i=0;i<data.ecd_with.length;i++){
                rop_ecdwith_datatable +='<tr><td>'+data.ecd_with[i].x+'</td><td>'+data.ecd_with[i].y+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            }
            rop_ecdwith_datatable +="</tbody></table></div>";
            
            rop_ecdwith_datatable +='<button class="ecd-button"><a href="' + rop_ecdwith_chart_url + '">Download <i class="fa fa-download icon-down"></a></button>';
            $('#rop_ecdwith_datatable').html(rop_ecdwith_datatable);

            // var rop_ecdwithout_datatable="";
            // rop_ecdwithout_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>Yield Point</h4></tr><tr><th>Yield Point</th><th>Pressure Loss</th></tr></thead><tbody>";
            // for(var i=0;i<data.ecd_without.length;i++){
            //     rop_ecdwithout_datatable +='<tr><td>'+data.ecd_without[i].x+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            // }
            // rop_ecdwithout_datatable +="</tbody></table></div>";
            // rop_ecdwithout_datatable +='<button><a href="' + rop_ecdwithout_chart_url + '">Download</a></button>';
            // $('#rop_ecdwithout_datatable').html(rop_ecdwithout_datatable);

        },
        complete: function(){
            $('#rop_ecd_chart').closest('div').find('.loading-gif').remove()
            createSVGFromChart(rop_ecd_chart, 'pressurelosschart_canvas','rop_ecd-'+wellphase_id+'-'+section_name);
        },
     
    });
}
function yieldpoint_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var download_url = $('#pressurelosschart-url').data('base-url');
    var yieldpoint_pressure_chart_url = download_url.replace('charttype', 'yieldpoint_pressure');
    var yieldpoint_pressure_chart_url = yieldpoint_pressure_chart_url.replace(0, wellphase_id);
    var yp = $('#yp_sensitivity').val()

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'yieldpoint_pressure',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
        $('#sensitivity_yieldpoint_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#sensitivity_yieldpoint_chart').css("text-align", "center");
        },
        success: function(data) {
            sensitivity_yieldpoint_chart(data) 
            sensitivity['sensitivity_yieldpoint_chart']=data

            var yieldpoint_pressure_datatable="";
            yieldpoint_pressure_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Yield Point</h4></tr><tr><th>Yield Point</th><th>Pressure Loss</th></tr></thead><tbody>";
            for(var i=0;i<data.result.length;i++){
                yieldpoint_pressure_datatable +='<tr><td>'+data.result[i].x+'</td><td>'+data.result[i].y+'</td></tr>';
            }
            yieldpoint_pressure_datatable +="</tbody></table></div>";
            yieldpoint_pressure_datatable +='<button class="ecd-button"><a href="' + yieldpoint_pressure_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#yieldpoint_pressure_datatable').html(yieldpoint_pressure_datatable);
        },
        complete: function(){
            $('#sensitivity_yieldpoint_chart').closest('div').find('.loading-gif').remove()
            createSVGFromChart(yeildpoint_chart, 'pressurelosschart_canvas','yieldpoint_pressure-'+wellphase_id+'-'+section_name);
        },
     
    });
}
function viscocity_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var yp = $('#yp_sensitivity').val()
    var download_url = $('#pressurelosschart-url').data('base-url');
    var viscocity_pressure_chart_url = download_url.replace('charttype', 'viscocity_pressure');
    var viscocity_pressure_chart_url = viscocity_pressure_chart_url.replace(0,wellphase_id);
    var viscocity_ecd_chart_url = download_url.replace('charttype', 'viscocity_ecd');
    var viscocity_ecd_chart_url = viscocity_ecd_chart_url.replace(0, wellphase_id);
   

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'viscocity_pressure',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
        $('#sensitivity_viscocity_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#sensitivity_viscocity_chart').css("text-align", "center");
        $('#viscocity_ecd_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#viscocity_ecd_chart').css("text-align", "center");
        
        },
        success: function(data) {
            sensitivity_viscocity_chart(data) 
            viscocityecdchart(data)
            sensitivity['sensitivity_viscocity_chart']=data

            var plastic_viscocity_ecd_datatable="";
            plastic_viscocity_ecd_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Plastic Viscocity</h4></tr><tr><th>Plastic Viscocity</th><th>ECD</th></tr></thead><tbody>";
            for(var i=0;i<data.ecd_without.length;i++){
                plastic_viscocity_ecd_datatable +='<tr><td>'+data.ecd_without[i].x+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            }
            plastic_viscocity_ecd_datatable +="</tbody></table></div>";
            plastic_viscocity_ecd_datatable +='<button class="ecd-button"><a href="' + viscocity_ecd_chart_url + '">Download <i class="fa fa-download icon-down"></a></button>';
            $('#plastic_viscocity_ecd_datatable').html(plastic_viscocity_ecd_datatable);
            createSVGFromChart(viscocity_ecd_chart, 'pressurelosschart_canvas','viscocity_ecd_chart-'+wellphase_id+'-'+section_name);


            var plastic_viscocity_pressure_datatable="";
            plastic_viscocity_pressure_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Plastic Viscocity</h4></tr><tr><th>Plastic Viscocity</th><th>Pressure loss</th></tr></thead><tbody>";
            for(var i=0;i<data.result.length;i++){
                plastic_viscocity_pressure_datatable +='<tr><td>'+data.result[i].x+'</td><td>'+data.result[i].y+'</td></tr>';
            }
            plastic_viscocity_pressure_datatable +="</tbody></table></div>";
            plastic_viscocity_pressure_datatable +='<button class="ecd-button"><a href="' + viscocity_pressure_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#plastic_viscocity_pressure_datatable').html(plastic_viscocity_pressure_datatable);
            createSVGFromChart(viscocity_sensitivity_chart, 'pressurelosschart_canvas','viscocity_pressure_chart-'+wellphase_id+'-'+section_name);
            
        },
        complete: function(){
            $('#sensitivity_viscocity_chart').closest('div').find('.loading-gif').remove()
            $('#viscocity_ecd_chart').closest('div').find('.loading-gif').remove()
            // createSVGFromChart(viscocity_chart, 'pressurelosschart_canvas','viscocity_chart-'+wellphase_id+'-'+section_name);
        },
     
    });
}
function tfa_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var yp = $('#yp_sensitivity').val()
    var download_url = $('#pressurelosschart-url').data('base-url');
    var tfa_pressure_chart_url = download_url.replace('charttype', 'tfa_pressure');
    var tfa_pressure_chart_url = tfa_pressure_chart_url.replace(0, wellphase_id);
    $.ajax({    
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'tfa_pressure',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
        $('#sensitivity_tfa_chart').html("<img src="+imgsrc+" class='loading-gif' />")
        $('#sensitivity_tfa_chart').css("text-align", "center");
        },
        success: function(data) {
            sensitivity_tfa_chart(data) 
            sensitivity['sensitivity_tfa_chart']=data
            
            var tfa_pressure_datatable="";
            tfa_pressure_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>TFA</h4></tr><tr><th>TFA</th><th>Pressure Loss</th><th>Bit pressure loss</th></tr></thead><tbody>";
            for(var i=0;i<data.result.length;i++){
                tfa_pressure_datatable +='<tr><td>'+data.result[i].x+'</td><td>'+data.result[i].y+'</td><td>'+data.bit_pressure_chart[i].y+'</td></tr>';
            }
            tfa_pressure_datatable +="</tbody></table></div>";
            tfa_pressure_datatable +='<button class="ecd-button"><a href="' + tfa_pressure_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#tfa_pressure_datatable').html(tfa_pressure_datatable);
            
        },
        complete: function(){
            $('#sensitivity_tfa_chart').closest('div').find('.loading-gif').remove()
            createSVGFromChart(tfachart,'pressurelosschart_canvas','tfa_pressure-'+wellphase_id+'-'+section_name);
        },
    });
}

function flowrate_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var download_url = $('#pressurelosschart-url').data('base-url');
    var flowrate_pressure_chart_url = download_url.replace('charttype', 'flowrate_pressure');
    var flowrate_pressure_chart_url = flowrate_pressure_chart_url.replace(0, wellphase_id);
    var flowrate_ecd_chart_url = download_url.replace('charttype', 'flowrate_ecd');
    var flowrate_ecd_chart_url = flowrate_ecd_chart_url.replace(0, wellphase_id);
    var yp = $('#yp_sensitivity').val()

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'flowrate_pressure',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
            if(type=='original'){
                $('#sensitivity_flowrate_chart').html("<img src="+imgsrc+" class='loading-gif' />")
                $('#sensitivity_flowrate_chart').css("text-align", "center");
                $('#flowrate_ecd_chart').html("<img src="+imgsrc+" class='loading-gif' />")
                $('#flowrate_ecd_chart').css("text-align", "center");
            }else{
                flowrate_pressure_chart.showLoading();
                flowrateecd.showLoading()

            }
        },
        success: function(data) {
            if(type=='original'){
                sensitivity_flowrate_chart(data) 
                flowrateecdchart(data)
                sensitivity['sensitivity_flowrate_chart']=data
            }
            else{
                sensitivity_flowrate_chart_changed(data)
                flowrateecdchart_changed(data)
            }

            var flowrate_ecd_datatable="";
            flowrate_ecd_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Flowrate</h4></tr><tr><th>Flowrate</th><th>ECD</th></tr></thead><tbody>";
            for(var i=0;i<data.ecd_without.length;i++){
                flowrate_ecd_datatable +='<tr><td>'+data.ecd_without[i].x+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            }
            flowrate_ecd_datatable +="</tbody></table></div>";
            flowrate_ecd_datatable +='<button class="ecd-button"><a href="' + flowrate_ecd_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#flowrate_ecd_datatable').html(flowrate_ecd_datatable);
            createSVGFromChart(flowrateecd, 'pressurelosschart_canvas','flowrate_ecd_chart-'+wellphase_id+'-'+section_name);
            var flowrate_pressure_datatable="";
            flowrate_pressure_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Flowrate</h4></tr><tr><th>Flowrate</th><th>Pressure Loss</th></tr></thead><tbody>";
            for(var i=0;i<data.result.length;i++){
                flowrate_pressure_datatable +='<tr><td>'+data.result[i].x+'</td><td>'+data.result[i].y+'</td></tr>';
            }
            flowrate_pressure_datatable +="</tbody></table></div>";
            flowrate_pressure_datatable +='<button class="ecd-button"><a href="' + flowrate_pressure_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#flowrate_pressure_datatable').html(flowrate_pressure_datatable);
            createSVGFromChart(flowrate_pressure_chart, 'pressurelosschart_canvas','flowrate_pressure_chart-'+wellphase_id+'-'+section_name);
           
        },
        complete: function(){
            if(type=='original'){
                $('#sensitivity_flowrate_chart').closest('div').find('.loading-gif').remove()
            }
            else{
                flowrate_pressure_chart.hideLoading();
                flowrateecd.hideLoading()
            }
            
            
        },
    });
}
function mudweight_pressure_calculation(wellphase_id,section_name,rpm,flowrate,rop,cuttings_density,cuttings_size,bitdepth,mudweight,plastic_viscocity,type,changedtype){
    var download_url = $('#pressurelosschart-url').data('base-url');
    var mudweight_pressure_chart_url = download_url.replace('charttype', 'mudweight_pressure');
    var mudweight_pressure_chart_url = mudweight_pressure_chart_url.replace(0,wellphase_id);
    var mudweight_ecd_chart_url = download_url.replace('charttype', 'mudweight_ecd');
    var mudweight_ecd_chart_url = mudweight_ecd_chart_url.replace(0,wellphase_id);
    var yp = $('#yp_sensitivity').val()

    $.ajax({
        type: "GET",
        url:"/pressureloss/sensitivity_calculation",
        cache: false,        
        data:{
            wellphase_id:wellphase_id,
            section_name:section_name,
            type:'mudweight_pressure',
            rpm:rpm,
            flowrate:flowrate,
            rop:rop,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            bitdepth:bitdepth,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            mudweight:mudweight,
            plastic_viscocity:plastic_viscocity,
            changedtype:changedtype,
            yp:yp
        },
        beforeSend: function() {
            if(type=='original'){
                $('#sensitivity_mudweight_chart').html("<img src="+imgsrc+" class='loading-gif' />")
                $('#sensitivity_mudweight_chart').css("text-align", "center");
                $('#mudweight_ecd_chart').html("<img src="+imgsrc+" class='loading-gif' />")
                $('#mudweight_ecd_chart').css("text-align", "center");
            }
            else{
                mudweight_pressure_chart.showLoading();
                mudweightecd_chart.showLoading();
            }
        
        
        },
        success: function(data) {
            if(type=='original'){
                sensitivity_mudweight_chart(data)
                mudweightecdchart(data)
                sensitivity['sensitivity_mudweight_chart']=data
            }                                                                        
            else{
                sensitivity_mudweight_chart_changed(data)
                mudweightecdchart_changed(data)
                sensitivity['sensitivity_mudweight_chart_changed']=data

            }
            var mudweight_ecd_datatable="";
            mudweight_ecd_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Mud Weight</h4></tr><tr><th>Mudweight</th><th>Pressure Loss</th></tr></thead><tbody>";
            for(var i=0;i<data.ecd_without.length;i++){
                mudweight_ecd_datatable +='<tr><td>'+data.ecd_without[i].x+'</td><td>'+data.ecd_without[i].y+'</td></tr>';
            }
            mudweight_ecd_datatable +="</tbody></table></div>";
            mudweight_ecd_datatable +='<button class="ecd-button"><a href="' + mudweight_ecd_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#mudweight_ecd_datatable').html(mudweight_ecd_datatable);
            createSVGFromChart(mudweightecd_chart,'pressurelosschart_canvas','mudweight_ecd-'+wellphase_id+'-'+section_name);

            var mudweight_pressure_datatable="";
            mudweight_pressure_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Mud Weight</h4></tr><tr><th>Mudweight</th><th>Pressure Loss</th></tr></thead><tbody>";
            for(var i=0;i<data.result.length;i++){
                mudweight_pressure_datatable +='<tr><td>'+data.result[i].x+'</td><td>'+data.result[i].y+'</td></tr>';
            }
            mudweight_pressure_datatable +="</tbody></table></div>";
            mudweight_pressure_datatable +='<button class="ecd-button"><a href="' + mudweight_pressure_chart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#mudweight_pressure_datatable').html(mudweight_pressure_datatable);
            createSVGFromChart(mudweight_pressure_chart,'pressurelosschart_canvas','mudweight_pressure-'+wellphase_id+'-'+section_name);
           
        },
        complete: function(){
            if(type=='original'){
                $('#sensitivity_mudweight_chart').closest('div').find('.loading-gif').remove()
                $('#mudweight_ecd_chart').closest('div').find('.loading-gif').remove()
            }
            else{
                mudweight_pressure_chart.hideLoading();
                mudweightecd_chart.hideLoading();
            }
            

        },
     
    });
}
function sensitivity_flowrate_chart(data){
    flowrate_pressure_chart=Highcharts.chart('sensitivity_flowrate_chart', {
            title: {
                text: 'Pressure Loss'
            },
            credits: {
                enabled: false
               },
            xAxis: {
                title: {
                    enabled: true,
                    text: 'Flowrate'
                },
                tickInterval : 50,

            },
            yAxis: {
                title: {
                    text: 'Pressure Loss'
                },
                tickInterval : 100,
                labels: {
                        format: '{value}'
                    },
            },

            plotOptions: {
                spline: {
                    marker: {
                        enabled: false
                    }
                }
            },
            
            series: [
            {
                type: 'spline',
                name: 'Total Pressure Loss',
                color: 'rgb(245,173,43)',
                data: data.result,
                dashStyle: 'Solid',
            }
        ]
        });
}
function sensitivity_mudweight_chart_changed(data){
    if ( !mudweight_pressure_chart.get( 'flowrate_mudweight' ) ) {
    mudweight_pressure_chart.addSeries({
        type: 'spline',
        name: 'Total Pressure Loss',
        color: 'rgb(245,173,43)',
        data: data.result,
        dashStyle: 'ShortDot',
        id:"flowrate_mudweight"
    })  
    }else{
        mudweight_pressure_chart.series[mudweight_pressure_chart.get('flowrate_mudweight').index].update({
            data: data.result
        });
    }
}
function mudweightecdchart_changed(data){
    if ( !mudweightecd_chart.get( 'mudweight_ecd_changed' ) ) {
        mudweightecd_chart.addSeries({
        type: 'spline',
        name: 'Total Pressure Loss',
        color: 'rgb(245,173,43)',
        data: data.ecd_without,
        dashStyle: 'ShortDot',
        id:"mudweight_ecd_changed"
    })  
    }else{
        mudweightecd_chart.series[mudweightecd_chart.get('mudweight_ecd_changed').index].update({
            data: data.ecd_without
        });
    }
}
function sensitivity_flowrate_chart_changed(data){
    if ( !flowrate_pressure_chart.get( 'mudweight_flowrate' ) ) {
        flowrate_pressure_chart.addSeries({
            type: 'spline',
            name: 'Total Pressure Loss',
            color: 'rgb(245,173,43)',
            data: data.result,
            dashStyle: 'ShortDot',
            id:"mudweight_flowrate"
        })  
    }else{
        flowrate_pressure_chart.series[flowrate_pressure_chart.get('mudweight_flowrate').index].update({
            data: data.result
        });
    }
}
function flowrateecdchart_changed(data){
    if ( !flowrateecd.get( 'flowrateecd_changed' ) ) {
        flowrateecd.addSeries({
            type: 'spline',
            name: 'Total Pressure Loss',
            color: 'rgb(245,173,43)',
            data: data.ecd_without,
            dashStyle: 'ShortDot',
            id:"flowrateecd_changed"
        })  
    }else{
        flowrateecd.series[flowrateecd.get('flowrateecd_changed').index].update({
            data: data.ecd_without
        });
    }
}

function sensitivity_mudweight_chart(data,type){
    mudweight_pressure_chart=Highcharts.chart('sensitivity_mudweight_chart', {
        title: {
            text: 'Pressure Loss'
        },
        credits: {
            enabled: false
           },
        xAxis: {
            title: {
                enabled: true,
                text: 'Mudweight'
            },
            tickInterval : 0.5,

        },
        yAxis: {
            title: {
                text: 'Pressure Loss'
            },
            tickInterval : 100,

        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        
        series: [
        {
            type: 'spline',
            name: 'Total Pressure Loss',
            color: 'rgb(245,173,43)',
            data: data.result,
            dashStyle: 'Solid',
        }
    ]
    });
   
}
function sensitivity_tfa_chart(data){
    tfachart=Highcharts.chart('sensitivity_tfa_chart', {
    title: {
        text: 'Pressure Loss'
    },
    credits: {
        enabled: false
       },
    xAxis: {
        title: {
            enabled: true,
            text: 'TFA'
        },
        tickInterval : 0.1,

    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value / 1000;
            }
        },
        title: {
            text: 'Pressure Loss (*1000)'
        },
        tickInterval : 100,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'Bit Pressure Loss',
        color: 'rgb(22,96,178)',
        data: data.bit_pressure_chart,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },
    {
        type: 'spline',
        name: 'Total Pressure Loss',
        color: 'rgb(22,96,178)',
        data: data.result,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
function sensitivity_viscocity_chart(data){
    viscocity_sensitivity_chart=Highcharts.chart('sensitivity_viscocity_chart', {
    title: {
        text: 'Pressure Loss'
    },
    credits: {
        enabled: false
       },
    xAxis: {
        title: {
            enabled: true,
            text: 'Plastic Viscocity'
        },
        tickInterval : 5,

    },
    yAxis: {
        labels: {
            format:'{value}'
        },
        title: {
            text: 'Pressure Loss'
        },
        tickInterval : 100,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'Total Pressure Loss',
        color: 'rgb(245,173,43)',
        data: data.result,
        dashStyle: 'Solid',
    }
  ]
});
}
function sensitivity_yieldpoint_chart(data){
    yeildpoint_chart=Highcharts.chart('sensitivity_yieldpoint_chart', {
    title: {
        text: 'Pressure Loss'
    },
    credits: {
        enabled: false
       },
    xAxis: {
        title: {
            enabled: true,
            text: 'Yield Point'
        },
        tickInterval : 5,

    },
    yAxis: {
        title: {
            text: 'Pressure Loss'
        },
        tickInterval : 100,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'Total Pressure Loss',
        color: 'rgb(245,173,43)',
        data: data.result,
        dashStyle: 'Solid',
    }
  ]
});
}
function flowrateecdchart(data){
    flowrateecd=Highcharts.chart('flowrate_ecd_chart', {
        title: {
            text: 'ECD'
        },
        credits: {
            enabled: false
           },
        xAxis: {
            title: {
                enabled: true,
                text: 'Flowrate'
            },
            tickInterval : 50,

        },
        yAxis: {
            title: {
                text: 'ECD'
            },
            tickInterval : 0.5,

        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        
        series: [
        {
            type: 'spline',
            name: 'ECD',
            color: 'rgb(22,96,178)',
            data: data.ecd_without,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
        },

    ]
    });
}
function mudweightecdchart(data){
    mudweightecd_chart=Highcharts.chart('mudweight_ecd_chart', {
        title: {
            text: 'ECD'
        },
        credits: {
            enabled: false
           },
        xAxis: {
            title: {
                enabled: true,
                text: 'Mud Weight'
            },
            tickInterval : 0.5,
    
        },
        yAxis: {
            title: {
                text: 'ECD'
            },
            tickInterval : 0.5,
    
        },
    
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        series: [
        {
            type: 'spline',
            name: 'ECD',
            color: 'rgb(22,96,178)',
            data: data.ecd_without,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
        },
    
    ]
    });
    
}
function viscocityecdchart(data){
    viscocity_ecd_chart = Highcharts.chart('viscocity_ecd_chart', {
    title: {
        text: 'ECD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'Plastic Viscocity'
        },
        tickInterval : 5,

    },
    yAxis: {
        title: {
            text: 'ECD'
        },
        tickInterval : 0.5,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'ECD',
        color: 'rgb(22,96,178)',
        data: data.ecd_without,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
function ropecdchart(data){
    rop_ecd_chart = Highcharts.chart('rop_ecd_chart', {
    title: {
        text: 'ECD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'ROP'
        },
        tickInterval : 10,
        min:0,
        max:200

    },
    yAxis: {
        title: {
            text: 'ECD'
        },
        tickInterval : 0.5,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'ECD(With Cuttings)',
        color: 'rgb(22,96,178)',
        data: data.ecd_with,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },
    {
        type: 'spline',
        name: 'ECD(Without Cuttings)',
        color: 'rgb(22,96,178)',
        data: data.ecd_without,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
function cuttingsdensityecdchart(data){
    cuttingsdensity_ecd_chart = Highcharts.chart('cuttingsdensity_ecd_chart', {
    title: {
        text: 'ECD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'Cuttings Density'
        },
        tickInterval : 0.5,
        min:19,
        max:25

    },
    yAxis: {
        title: {
            text: 'ECD'
        },
        tickInterval : 0.5,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'ECD(With Cuttings)',
        color: 'rgb(22,96,178)',
        data: data.ecd_with,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },
    {
        type: 'spline',
        name: 'ECD(Without Cuttings)',
        color: 'rgb(22,96,178)',
        data: data.ecd_without,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
function cuttingssizeecdchart(data){
    cuttingssize_ecd_chart = Highcharts.chart('cuttingssize_ecd_chart', {
    title: {
        text: 'ECD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'Cuttings Size'
        },
        tickInterval : 0.05,
        min:0,
        max:1

    },
    yAxis: {
        title: {
            text: 'ECD'
        },
        tickInterval : 0.5,

    },

    plotOptions: {
        spline: {
            marker: {
                enabled: false
            }
        }
    },
    
    series: [
    {
        type: 'spline',
        name: 'ECD(Without Cuttings)',
        color: 'rgb(22,96,178)',
        data: data.ecd_without,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },
    {
        type: 'spline',
        name: 'ECD(With Cuttings)',
        color: 'rgb(22,96,178)',
        data: data.ecd_with,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
// sensitivity_unitchange(sensitivity);