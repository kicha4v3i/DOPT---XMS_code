var ann_drill_chart
var ann_array = [0,0,0]
var drill_array = [0,0,0]
ann_drill_chart = Highcharts.chart('drillstring_annular', {
    chart: {
        type: 'bar',
        width: 400,
        height: 350
    },
    title: {
        text: 'Drillstring and Annular losses'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        // categories: ['N', 'BP', 'PL', 'HB'],
        categories: ['BP', 'PL','HB'],
        title: {
            text: 'Annular and DrillString Loss'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '',
            align: 'high'
        },
        // minorGridLineWidth: 0,
        // lineColor: 'transparent',
        // labels: {
        //     enabled: false
        // },
        labels: {
            formatter: function () {
                return this.value +display_pressureunit;
            }
        }
    },
    tooltip: {
        valueSuffix: ''
    },
    plotOptions: {
        bar: {
            pointWidth:5,
            dataLabels: {
                enabled: true,
                format: '{y} ' + display_pressureunit,
                style:{
                    color:'gray'
                }
            }
        }
    },
    legend: {
        // layout: 'vertical',
        // align: 'right',
        // verticalAlign: 'top',
        // x: -40,
        // y: 80,
        // floating: true,
        // borderWidth: 1,
        // backgroundColor:
        //     Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
        // shadow: true
    },
    credits: {
        enabled: false
    },
    series: [{
        id: 'Drillstring',
        name: 'Drillstring',
        data: [],
        color: {
        linearGradient: {
                x1: 0,
                x2: 0,
                y1: 1,
                y2: 0
                },
                stops: [
                [0, '#3EA1B8'],
                [1, '#6BE5F2']
                ]
            }

    
    },
    {
        id: 'Annulus',
        name: 'Annulus',
        data:[],
        color: {
        linearGradient: {
                x1: 0,
                x2: 0,
                y1: 1,
                y2: 0
                },
                stops: [
                [0, '#944ED3 '],
                [1, '#BC85FD']
                ]
            }
    } 
]
});

$('.allmodel_change_unit').click(function(){
    alert("dshcv")
    console.log("comparison"+comparison)
    getallmodalunit(comparison);
});

$(document).on("click", ".comparison" , function() {
    var flowrate=$('.flowrate').val();
    var rpm=$('.rpm').val();
    var rop=$('.rop').val();

    if(flowrate!='' && rpm!=''){
        comparison['flowrate']=flowrate
        comparison['rpm']=rpm
        comparison['rop']=rop
        comparison['bit_depth']=$('#bitdepth_userenter').val()

        getallbingham_loss(rpm,flowrate)
        getallpowerlaw_loss(rpm,flowrate)
        getallbit_loss(rpm,flowrate)
        getallhersel_loss(rpm,flowrate,rop)
        
        // getallmodel_surface(rpm,flowrate)
        // getallmodel_annular(rpm,flowrate)
        
        //getallmodellosses(rpm,flowrate) 
    }
});

function getallbit_loss(rpm,flowrate){
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var rop=$('#rop_userenter').val();
    var bitdepth=$('#bitdepth_userenter').val()
    data={
        rpm:rpm,
        flowrate:flowrate,
        wellphase_id:wellphase_id,
        section_name:section_name,
        rop:rop,
        bitdepth:bitdepth,
    }
 
    return new Promise((resolve, reject) => {
        fetch("/pressureloss/calculatebitpressureloss",{method: 'POST', body:  JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        })
        .then(response => response.json())
        .then(data => {
            resolve(data)
            comparison['pv']=data.pv
            comparison['yp']=data.yp
            comparison['K']=data.K
            comparison['n']=data.m
            comparison['bit_losses']=data.bit_losses
            comparison['mudweight']=data.mudweight
            comparison['selected_model']=data.selected_modal

            var total_details=""
            total_details +='<h4 class="head-tlt">Total Pressure Loss</h4>'
            total_details +='<table class="total-loss"><tr><td><span class="value-colr"><input type="number" step="any" name="flowrate_data" value='+flowrate+' id="flowrate_data" class="form-control flowrate_data edit-vlu"></span>' +display_flowrateunit+ '<br>Flowrate</td><td> <span class="value-colr"><input type="number" step="any" name="rpm_data" id="rpm_data" value='+rpm+' class="form-control rpm_data edit-vlu"></span> rpm<br>RPM</td></tr>'
            total_details +='<tr><td> <span class="value-colr">'+data.todepth+'</span>' + display_depthunit + '<br>Bit Depth</td><td><span class="value-colr">'+rop+'</span>' + display_depthunit+ '/hr<br>ROP</td></tr>'
            $('#total_details').html(total_details)

            var rheogram_mudparameter=""
            rheogram_mudparameter +='<table class="rmp-tbl">'
            rheogram_mudparameter +='<h4 class="rmp-txt">Rheology and Mud Parameters</h4>'
            rheogram_mudparameter +='<tr><th>Mud Weight</th><td>'+data.mudweight+display_densityunit + '</td></tr>'
            rheogram_mudparameter +='<tr><th>Rheology</th><td>'+data.selected_modal+'</td></tr>'
            rheogram_mudparameter +='<tr><th>PV / YP</th><td>'+data.pv+display_plastic_viscosity+'/ '+data.yp+display_gelstrengthunit+'</td></tr>'
            rheogram_mudparameter +='<tr><th>n/K</th><td>'+data.K+' / '+data.m+'</td></tr>'
            rheogram_mudparameter +='</table>'
            $('#rheogram_mudparameter').html(rheogram_mudparameter)

            

            var drillbit =''
            drillbit +='<h5 class="head-tlt">Bit Hydraulics</h5><div><table class="bh-tbl">'
            drillbit +='<tr><th>Bit Pressure Loss</th><td>'+data.bit_losses[0].bit_pressure_loss.toFixed()+display_pressureunit +'</td></tr>'
            drillbit +='<tr><th>Impact Force</th><td>'+data.bit_losses[0].impact_forces.toFixed()+display_impactforce+'</td></tr>'
            drillbit +='<tr><th>Jet Velocity</th><td>'+data.bit_losses[0].jet_velocity.toFixed()+' <sup>'+display_diameter+'</sup>/<sub>sec</sub></td></tr>'
            drillbit +='<tr><th>BHHP</th><td>'+data.bit_losses[0].bhhp.toFixed()+display_bhhp +'</td></tr>'
            drillbit +='<tr><th>HSI</th><td>'+data.bit_losses[0].hsi.toFixed(2)+'  <sup>'+ display_bhhp +'</sup>/'+display_diameter+'<sub>2</sub></td></tr>'
            drillbit +='<tr><th>TFA</th><td>'+data.bit_losses[0].tfa_value.toFixed(2)+display_diameter+'<sup>2</sup></td></tr>'
            drillbit +='<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse">Nozzle Details</a></td></table>';
            drillbit +=`<div class="collapse first"><div class="block__content" id='nozzles-detail'></div></div>`
            $('#drill-bit').html(drillbit)

        })
        .catch(error => {
        reject(error); 
        });
    });
}

function getallhersel_loss(rpm,flowrate,rop){
    var rop=$('#rop_userenter').val()
    $.ajax({
        type: "GET",
        url:"/pressureloss/getallherselmodel",
        data:{
            rpm:rpm,
            flowrate:flowrate,
            wellphase_id:wellphase_id,
            section_name:section_name,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            rop:rop
        },
        success: function(data) {

            var series = {
                name:'All Hersel Loss',
                data: [0,0,data.allhershel_pressureloss],
                color: {
                    linearGradient: {
                        x1: 0,
                        x2: 0,
                        y1: 1,
                        y2: 0
                    },
                    stops: [
                        [0, '#FAD169 '],
                        [1, '#FCE766']
                    ]

                },
            }

            checkseries=isSeriesExists('All Hersel Loss',allmodalchart)
            if(checkseries==false){
            allmodalchart.addSeries(series)
            }
            var totalsurface=0
            comparison['hershel_surface_losses']=data.hershel_surface_losses
            comparison['ty']=data.ty

            comparison['hershelannular']=data.allhershel.totalannular_pressureloss
            comparison['hersheldrillstring']=data.allhershel.totaldrillstring_pressureloss

            comparison['allhershel_pressureloss']=data.allhershel_pressureloss

            if ($('.surface-tbl').length) {
                var count=0
                $(".surface-tbl tbody tr").each(function() {
                    var columnIndex = 5; 
                    $(this).find("td").eq(columnIndex).each(function() {
                        totalsurface += Math.round(data.hershel_surface_losses[count].pressureloss)
                        var currentData = Math.round(data.hershel_surface_losses[count].pressureloss)+display_pressureunit;
                        $(this).html(currentData);
                    });
                    count =count+1;
                });

            }  
            else 
            {
                all_surface=''
                all_surface +="<div class='card p-3'><table class='table surface-tbl'><thead><tr><th>Element</th><th>ID</th><th>Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
                all_surface +='<tr><th></th><th></th><th></th><th id="surface_bingham"></th><th id="surface_powerlaw"></th><th id="surface_hershel"></th></tr>'
                all_surface +='</thead>';
                all_surface +='<tbody>';

                for(var i=0;i<data.hershel_surface_losses.length;i++){
                    all_surface +='<tr>';
                    all_surface +='<td>'+data.hershel_surface_losses[i].type+'</td>';
                    all_surface +='<td>'+data.hershel_surface_losses[i].id+display_diameter + '</td>';
                    all_surface +='<td>'+data.hershel_surface_losses[i].length+ display_depthunit + '</td>';
                
                    all_surface +='<td></td>';
                    all_surface +='<td></td>'
                    all_surface +='<td>'+Math.round(data.hershel_surface_losses[i].pressureloss)+display_pressureunit + '</td>';
                    totalsurface +=Math.round(data.hershel_surface_losses[i].pressureloss)
                    all_surface +='</tr>'  
                }
                all_surface +='</tbody></table>';
                $('#allsurface-loss').html(all_surface)
               
             
                

            }
            $('#surface_hershel').html(totalsurface.toFixed()+display_pressureunit)

            comparison['hershel_drillannulur_losses']=data.hershel_annular_pressure_loss.allpressureloss
            if ($('.drilling-tbl').length) {
                var count=0
                total_drill=0

                $(".drilling-tbl tbody tr").each(function() {
                    var columnIndex = 5; 
                    $(this).find("td").eq(columnIndex).each(function() {
                        var currentData =data.hershel_annular_pressure_loss.allpressureloss[count].drillstringloss.toFixed();
                        total_drill += parseFloat(currentData)

                        $(this).html(currentData+display_pressureunit);
                    });
                    count =count+1;
                });

            }  
            else {
                var all_drillstring_losses = ''
                all_drillstring_losses +="<table class='table drilling-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"


                all_drillstring_losses +='<tr><th></th><th></th><th></th><th id="drill_bingham"></th><th id="drill_powerlaw"></th><th id="drill_hershel"></th></tr>'
                all_drillstring_losses +="</thead>"

                all_drillstring_losses +='<tbody>';
                const drill_loss=data.hershel_annular_pressure_loss.allpressureloss
                var total_drill=0
                for(var i=drill_loss.length-1;i>=0;i--){
                    all_drillstring_losses +='<tr>';
                    all_drillstring_losses +='<td><span class='+drill_loss[i].element_type+'>'+drill_loss[i].element_type+'</span></td>';
                    all_drillstring_losses +='<td>'+drill_loss[i].element+'</td>';
                    all_drillstring_losses +='<td>'+drill_loss[i].od+display_diameter+ '/ '+drill_loss[i].id+display_diameter + '/ '+drill_loss[i].length_against.toFixed(2)+display_depthunit +'</td>';
                    total_drill += parseFloat(drill_loss[i].drillstringloss)
                    all_drillstring_losses +='<td></td>';
                    all_drillstring_losses += '<td> </td>'
                    all_drillstring_losses +='<td>'+drill_loss[i].drillstringloss.toFixed()+display_pressureunit +'</td>';

                    all_drillstring_losses +='</tr>'
                }
                all_drillstring_losses +='</tbody></table>';
                $('#allpipe-loss').html(all_drillstring_losses)


            }
            $('#drill_hershel').html(total_drill.toFixed()+display_pressureunit)



            if ($('.annuls-tbl').length) {                
                var count=0
                var total_ann=0
                $(".annuls-tbl tbody tr").each(function() {
                    var columnIndex = 6; 

                    $(this).find("td").eq(columnIndex).each(function() {
                        var currentData =data.hershel_annular_pressure_loss.allpressureloss[count].pressureloss.toFixed();
                        total_ann += parseFloat(currentData)
                        $(this).html(currentData+display_pressureunit);
                    });
                    count =count+1;
                });
            }  
            else {
            var allannularlosses=''
            cumulative_length=0
            allannularlosses +="<table class='table annuls-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th>Cumulative Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
            allannularlosses +='<tr><th></th><th></th><th></th><th></th><th id="annulus_bingham"></th><th id="annulus_powerlaw"></th><th id="annulus_hershel"></th></tr>'
            allannularlosses +='</thead>'

            var total_ann = 0
            allannularlosses += '<tbody>'

            const annular_loss=data.hershel_annular_pressure_loss.allpressureloss

            for(var i=annular_loss.length-1;i>=0;i--){
                allannularlosses +='<tr>';
                allannularlosses +='<td><span class='+annular_loss[i].element_type+'>'+annular_loss[i].element_type+'</span></td>';
                allannularlosses +='<td>'+annular_loss[i].element+'</td>';
                allannularlosses +='<td>'+annular_loss[i].od+display_diameter +'/ '+annular_loss[i].id+display_diameter+'/ '+annular_loss[i].length_against.toFixed(0)+display_depthunit+ '</td>';
                allannularlosses +='<td>'+annular_loss[i].cumlativelength.toFixed(0)+display_depthunit+ '</td>';
                total_ann += parseFloat(annular_loss[i].pressureloss)
                allannularlosses +='<td></td>';
                allannularlosses += '<td></td>'
                allannularlosses +='<td>'+annular_loss[i].pressureloss.toFixed()+display_pressureunit+ '</td>';

                allannularlosses +='</tr>'
            }
            allannularlosses +='</tbody></table>';
            $('#allAnnular-loss').html(allannularlosses);
            drill_array[2]=total_drill
            ann_array[2]=total_ann


            var series0 = ann_drill_chart.series[0];
            var series1 = ann_drill_chart.series[1];
    
            series0.setData(drill_array);
            series1.setData(ann_array);
            ann_drill_chart.redraw();
        }
        $('#annulus_hershel').html(total_ann.toFixed()+display_pressureunit)


        },
        error: function (err) {
            console.log(err)
        },   
    })
}

function getallbingham_loss(rpm,flowrate){
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var rop=$('#rop_userenter').val();
    $.ajax({
        type: "GET",
        url:"/pressureloss/getallbingham",
        data:{
            rpm:rpm,
            flowrate:flowrate,
            wellphase_id:wellphase_id,
            section_name:section_name,
            rop:rop
        },
        success: function(data) {
    
            comparison['binghamannular']=data.data.allbingham.totalannular_pressureloss
            comparison['binghamdrillstring']=data.data.allbingham.totaldrillstring_pressureloss
            comparison['allbingham_pressureloss']=data.data.allbingham_pressureloss


            
            var series = {
                name:'All Bingham Loss',
                data: [data.data.allbingham_pressureloss,0,0],
                color: {
                   linearGradient: {
                           x1: 0,
                           x2: 0,
                           y1: 1,
                           y2: 0
                           },
                           stops: [
                           [0, '#1AB099 '],
                           [1, '#28DFC2']
                           ]
                       },
             }

             checkseries=isSeriesExists('All Bingham Loss',allmodalchart)
             if(checkseries==false){
                allmodalchart.addSeries(series)
             }
             var totalsurface=0
            comparison['bingham_surface_losses']=data.data.bingham_surface_losses
            if ($('.surface-tbl').length) {

                
                var count=0

                $(".surface-tbl tbody tr").each(function() {
                var columnIndex = 3; 

                $(this).find("td").eq(columnIndex).each(function() {
                    var currentData = Math.round(data.data.bingham_surface_losses[count].pressureloss)+display_pressureunit;
                    totalsurface += Math.round(data.data.bingham_surface_losses[count].pressureloss)

                    $(this).html(currentData);
                 });
                 count =count+1;

                   
            });

            }  else {

                all_surface=''
                all_surface +="<div class='card p-3'><table class='table surface-tbl'><thead><tr><th>Element</th><th>ID</th><th>Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
                all_surface +='<tr><th></th><th></th><th></th><th id="surface_bingham"></th><th id="surface_powerlaw"></th><th id="surface_hershel"></th></tr>'
                all_surface +='</thead>';

                all_surface +='<tbody>';
                for(var i=0;i<data.data.bingham_surface_losses.length;i++){
                    all_surface +='<tr>';
                    all_surface +='<td>'+data.data.bingham_surface_losses[i].type+'</td>';
                    all_surface +='<td>'+data.data.bingham_surface_losses[i].id+display_diameter + '</td>';
                    all_surface +='<td>'+data.data.bingham_surface_losses[i].length+ display_depthunit + '</td>';
                
                    all_surface +='<td>'+Math.round(data.data.bingham_surface_losses[i].pressureloss)+display_pressureunit + '</td>';
                    all_surface +='<td> </td>'
                    all_surface +='<td> </td>'
                    totalsurface += Math.round(data.data.bingham_surface_losses[i].pressureloss)
                    all_surface +='</tr>'  
                
            }
            console.log("totalsurface"+totalsurface)
            all_surface +='</tbody></table>';
            $('#allsurface-loss').html(all_surface)

            

        }
        $('#surface_bingham').html(totalsurface.toFixed()+display_pressureunit)

        comparison['bingham_drillannulur_losses']=data.data.bingham_annular_pressure_loss.allpressureloss

        if ($('.drilling-tbl').length) {

            
                var count=0
                total_drill=0

                $(".drilling-tbl tbody tr").each(function() {
                var columnIndex = 3; 
                

                $(this).find("td").eq(columnIndex).each(function() {
                    var currentData =data.data.bingham_annular_pressure_loss.allpressureloss[count].drillstringloss.toFixed();
                    total_drill += parseFloat(currentData)

                    $(this).html(currentData+display_pressureunit);
                 });
                 count =count+1;

                   
            });

            }  else {
                var all_drillstring_losses = ''

            all_drillstring_losses +="<table class='table drilling-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"

            all_drillstring_losses +='<tr><th></th><th></th><th></th><th id="drill_bingham"></th><th id="drill_powerlaw"></th><th id="drill_hershel"></th></tr>'
            
            all_drillstring_losses +='</thead>';
            
            all_drillstring_losses +='<tbody>';
            const drill_loss=data.data.bingham_annular_pressure_loss.allpressureloss
            var total_drill=0
            for(var i=drill_loss.length-1;i>=0;i--){
                all_drillstring_losses +='<tr>';
                all_drillstring_losses +='<td><span class='+drill_loss[i].element_type+'>'+drill_loss[i].element_type+'</span></td>';
                all_drillstring_losses +='<td>'+drill_loss[i].element+'</td>';
                all_drillstring_losses +='<td>'+drill_loss[i].od+display_diameter+ '/ '+drill_loss[i].id+display_diameter + '/ '+drill_loss[i].length_against.toFixed(2)+display_depthunit +'</td>';
                total_drill += parseFloat(drill_loss[i].drillstringloss)
                all_drillstring_losses +='<td>'+drill_loss[i].drillstringloss.toFixed()+display_pressureunit +'</td>';
                all_drillstring_losses += '<td> </td>'
                all_drillstring_losses +='<td> </td>'

                all_drillstring_losses +='</tr>'
             }
            all_drillstring_losses +='</tbody></table>';
            
            $('#allpipe-loss').html(all_drillstring_losses)

        }
        $('#drill_bingham').html(total_drill.toFixed()+display_pressureunit)

        
            

            if ($('.annuls-tbl').length) {
                
                var count=0
                var total_ann=0
                $(".annuls-tbl tbody tr").each(function() {
                var columnIndex = 4; 
                $(this).find("td").eq(columnIndex).each(function() {
                    var currentData =data.data.bingham_annular_pressure_loss.allpressureloss[count].pressureloss.toFixed();
                    total_ann += parseFloat(currentData)
                    $(this).html(currentData+display_pressureunit);
                 });
                 count =count+1;

                   
            });
            }  else {
            var allannularlosses=''
            cumulative_length=0
            allannularlosses +="<table class='table annuls-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th>Cumulative Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
            allannularlosses +='<tr><th></th><th></th><th></th><th></th><th id="annulus_bingham"></th><th id="annulus_powerlaw"></th><th id="annulus_hershel"></th></tr>'
            allannularlosses +='</thead>'
            var total_ann = 0
            allannularlosses += '<tbody>'

            const annular_loss=data.data.bingham_annular_pressure_loss.allpressureloss

            for(var i=annular_loss.length-1;i>=0;i--){
                // cumulative_length=cumulative_length+annular_loss[i].length
                allannularlosses +='<tr>';
                allannularlosses +='<td><span class='+annular_loss[i].element_type+'>'+annular_loss[i].element_type+'</span></td>';
                allannularlosses +='<td>'+annular_loss[i].element+'</td>';
                allannularlosses +='<td>'+annular_loss[i].od+display_diameter +'/ '+annular_loss[i].id+display_diameter+'/ '+annular_loss[i].length_against.toFixed(0)+display_depthunit+ '</td>';
                allannularlosses +='<td>'+annular_loss[i].cumlativelength.toFixed(0)+display_depthunit+ '</td>';
                total_ann += parseFloat(annular_loss[i].pressureloss)
                allannularlosses +='<td>'+annular_loss[i].pressureloss.toFixed()+display_pressureunit+ '</td>';
                allannularlosses += '<td> </td>'
                allannularlosses += '<td> </td>'

                allannularlosses +='</tr>'
            }
            allannularlosses +='</tbody></table>';
            $('#allAnnular-loss').html(allannularlosses);

            
        }
        $('#annulus_bingham').html(total_ann.toFixed()+display_pressureunit)

       
      
        drill_array[0]=total_drill
        ann_array[0]=total_ann
     
        var series0 = ann_drill_chart.series[0];
        var series1 = ann_drill_chart.series[1];

        series0.setData(drill_array);
        series1.setData(ann_array);
        ann_drill_chart.redraw();


        }
    })
}
function getallpowerlaw_loss(rpm,flowrate){
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var rop=$('#rop_userenter').val();
    $.ajax({
        type: "GET",
        url:"/pressureloss/getallpowerlaw",
        data:{
            rpm:rpm,
            flowrate:flowrate,
            wellphase_id:wellphase_id,
            section_name:section_name,
            rop:rop
        },
        success: function(data) {
            var series = {
                name:'All powerlaw loss',
                data: [0,data.data.allpowerlaw_pressureloss,0],
                color: {
                    linearGradient: {
                        x1: 0,
                        x2: 0,
                        y1: 1,
                        y2: 0
                    },
                    stops: [
                    [0, '#1D8B38 '],
                    [1, '#45DA6A']
                    ]
                },

            }   
            checkseries=isSeriesExists('All powerlaw loss',allmodalchart)
            if(checkseries==false){
                allmodalchart.addSeries(series)
            }
            var totalsurface=0
            comparison['powerlaw_surface_losses']=data.data.powerlaw_surface_losses

            comparison['powerlawannular']=data.data.allpowerlaw.totalannular_pressureloss
            comparison['powerlawdrillstring']=data.data.allpowerlaw.totaldrillstring_pressureloss
            comparison['allpowerlaw_pressureloss']=data.data.allpowerlaw_pressureloss


            if ($('.surface-tbl').length) {
                var count=0
                var columnIndex = 4;
                $(".surface-tbl tbody tr").each(function() {
                    $(this).find("td").eq(columnIndex).each(function() {
                        var currentData = Math.round(data.data.powerlaw_surface_losses[count].pressureloss)+display_pressureunit;
                        totalsurface +=Math.round(data.data.powerlaw_surface_losses[count].pressureloss)

                        $(this).html(currentData);
                    });
                    count =count+1;
                });

            } else {
                all_surface=''
                all_surface +="<div class='card p-3'><table class='table surface-tbl'><thead><tr><th>Element</th><th>ID</th><th>Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
                all_surface +='<tr><th></th><th></th><th></th><th id="surface_bingham"></th><th id="surface_powerlaw"></th><th id="surface_hershel"></th></tr>'
                all_surface +='</thead>';
                all_surface +='<tbody>';
                for(var i=0;i<data.data.powerlaw_surface_losses.length;i++){
                    all_surface +='<tr>';
                    all_surface +='<td>'+data.data.powerlaw_surface_losses[i].type+'</td>';
                    all_surface +='<td>'+data.data.powerlaw_surface_losses[i].id+display_diameter+'</td>';
                    all_surface +='<td>'+data.data.powerlaw_surface_losses[i].length+display_depthunit+'</td>';
                    all_surface +='<td> </td>'
                    all_surface +='<td>'+Math.round(data.data.powerlaw_surface_losses[i].pressureloss)+display_pressureunit+'</td>';
                    all_surface +='<td> </td>'
                    totalsurface +=Math.round(data.data.powerlaw_surface_losses[i].pressureloss)
                    all_surface +='</tr>'  
                }
                all_surface +='</tbody></table>';
                $('#allsurface-loss').html(all_surface)
                console.log("totalsurface"+totalsurface)

             
            }
            $('#surface_powerlaw').html(totalsurface.toFixed()+display_pressureunit)
            comparison['powerlaw_drillannulur_losses']=data.data.powerlaw_annular_pressure_loss.allpressureloss

            if ($('.drilling-tbl').length) {
                var count=0
                var total_drill=0
                $(".drilling-tbl tbody tr").each(function() {
                    var columnIndex = 4; 
                    $(this).find("td").eq(columnIndex).each(function() {
                        var currentData = data.data.powerlaw_annular_pressure_loss.allpressureloss[count].drillstringloss;
                        total_drill+=parseFloat(currentData)
                        $(this).html(currentData.toFixed()+display_pressureunit);
                    });
                    count =count+1;
                });

            } else {
                var all_drillstring_losses = ''
                var total_drill=0
                all_drillstring_losses +="<table class='table drilling-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
            
                all_drillstring_losses +='<tr><th></th><th></th><th></th><th id="drill_bingham"></th><th id="drill_powerlaw"></th><th id="drill_hershel"></th></tr>'
                all_drillstring_losses +='</thead>';

                all_drillstring_losses +='<tbody>';
                const drill_loss=data.data.powerlaw_annular_pressure_loss.allpressureloss
            
                for(var i=drill_loss.length-1;i>=0;i--){
                    all_drillstring_losses +='<tr>';
                    all_drillstring_losses +='<td><span class='+drill_loss[i].element_type+'>'+drill_loss[i].element_type+'</span></td>';
                    all_drillstring_losses +='<td>'+drill_loss[i].element+'</td>';
                    all_drillstring_losses +='<td>'+drill_loss[i].od+display_diameter+'/ '+drill_loss[i].id+display_diameter+'/ '+drill_loss[i].length_against.toFixed(2)+display_depthunit+'</td>';
                    all_drillstring_losses += '<td> </td>'
                    total_drill += parseFloat(drill_loss[i].drillstringloss)
                    all_drillstring_losses +='<td>'+drill_loss[i].drillstringloss.toFixed()+display_pressureunit+'</td>';
                    all_drillstring_losses += '<td> </td>'

                    all_drillstring_losses +='</tr>'
                }
                all_drillstring_losses +='</tbody></table>';
                
                $('#allpipe-loss').html(all_drillstring_losses)
            }
            $('#drill_powerlaw').html(total_drill.toFixed()+display_pressureunit)

            
      

            if ($('.annuls-tbl').length) {
                var count=0
                var total_ann = 0
                $(".annuls-tbl tbody tr").each(function() {
                    var columnIndex = 5; 
                    $(this).find("td").eq(columnIndex).each(function() {
                        var currentData =data.data.powerlaw_annular_pressure_loss.allpressureloss[count].pressureloss;
                        total_ann += parseFloat(currentData)
                        $(this).html(currentData.toFixed()+display_pressureunit);
                    });
                    count =count+1;
                });

            }  else {
                var allannularlosses=''
                var total_ann = 0
            cumulative_length=0
            allannularlosses +="<table class='table annuls-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th>Cumulative Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th><th class='hershel-clr'>Hershel</th></tr>"
            allannularlosses +='<tr><th></th><th></th><th></th><th></th><th id="annulus_bingham"></th><th id="annulus_powerlaw"></th><th id="annulus_hershel"></th></tr>'
            allannularlosses +='</thead>'
            
            allannularlosses += '<tbody>'

            const annular_loss=data.data.powerlaw_annular_pressure_loss.allpressureloss

            for(var i=annular_loss.length-1;i>=0;i--){
                allannularlosses +='<tr>';
                allannularlosses +='<td><span class='+annular_loss[i].element_type+'>'+annular_loss[i].element_type+'</span></td>';
                allannularlosses +='<td>'+annular_loss[i].element+'</td>';
                allannularlosses +='<td>'+annular_loss[i].od+display_diameter+'/ '+annular_loss[i].id+display_diameter+'/ '+annular_loss[i].length_against.toFixed(0)+display_depthunit+'</td>';
                allannularlosses +='<td>'+annular_loss[i].cumlativelength.toFixed(0)+display_depthunit+'</td>';
                allannularlosses += '<td> </td>'
                total_ann += parseFloat(annular_loss[i].pressureloss)
                allannularlosses +='<td>'+annular_loss[i].pressureloss.toFixed()+' {%display_pressureunit request.session.unit%}</td>';
                allannularlosses += '<td> </td>'

                allannularlosses +='</tr>'
            }
            allannularlosses +='</tbody></table>';
            $('#allAnnular-loss').html(allannularlosses);

        }
        $('#annulus_powerlaw').html(total_ann.toFixed()+display_pressureunit)

        drill_array[1]=total_drill
        ann_array[1]=total_ann
      
        var series0 = ann_drill_chart.series[0];
        var series1 = ann_drill_chart.series[1];

        series0.setData(drill_array);
        series1.setData(ann_array);
        ann_drill_chart.redraw();
        

       
  
        }
    })

}

function getallmodalunit(data){
    if (data.unit == 'API'){
        var pressure = ' kPa';
        var depth = 'm';
        var length = 'm';
        var diameter = 'mm';
        var flowrate = 'LPF';
        var mud_weight = 'g/cc';
        var nozzlesize = 'mm';
        var tfa = 'mm<sup>2</sup>';
        var bhhp = 'hp';
        var hsi = 'hp/in<sup>2</sup>';
        var rop = 'm/hr';
        var impact = 'lbf';
        var jetvelocity = 'ft/sec';
        var viscocity = 'Pa.sec';
        var yeildpoint = 'Pa';
    }
    else{
        var pressure = ' psi';
        var depth = ' ft';
        var length = ' ft';
        var diameter = ' in';
        var flowrate = ' GPM';
        var mud_weight = ' ppg';
        var nozzlesize = ' 1/32in';
        var tfa = ' in<sup>2</sup>';
        var bhhp = 'kW';
        var hsi = 'kW/mm<sup>2</sup>';
        var impact = 'N';
        var rop = ' ft/hr';
        var jetvelocity = 'm/sec';
        var viscocity = ' cP';
        var yeildpoint = ' lbf/100ft^2';
    }
    
    var totalannular =[];
    var totaldrillstring =[];
    var totalannular_newtonian_loss = 0
    var totalannular_bingham_loss = 0
    var totalannular_powerlaw_loss = 0
    var totalannular_hershel_loss = 0
    var totaldrillstring_newtonian =0
    var totaldrillstring_bingham =0
    var totaldrillstring_powerlaw =0
    var totaldrillstring_hershel =0
    var total_surface_newtonian=0
    var total_surface_bingham=0
    var total_surface_powerlaw=0
    var total_surface_hershel=0

    var total_details=""
    total_details +='<h4 class="head-tlt">Total Pressure Loss</h4>'
    if (data.unit == 'API'){
        total_details +='<table class="total-loss"><tr><td><span class="value-colr"><input type="number" step="any" name="flowrate_data" value='+(data.flowrate*3.78).toFixed()+' id="flowrate_data" class="form-control flowrate_data edit-vlu"></span> '+flowrate+'<br>Flowrate</td><td> <span class="value-colr"><input type="number" step="any" name="rpm_data" id="rpm_data" value='+data.rpm+' class="form-control rpm_data edit-vlu"></span> rpm<br>RPM</td></tr>'
        total_details +='<tr><td> <span class="value-colr">'+(data.bit_depth/3.281).toFixed()+'</span> '+depth+'<br>Bit Depth</td><td><span class="value-colr">'+(data.rop/3.281).toFixed(2)+'</span>'+rop+'<br>ROP</td></tr>'
    }
    else{
        total_details +='<table class="total-loss"><tr><td><span class="value-colr"><input type="number" step="any" name="flowrate_data" value='+(data.flowrate*0.2647).toFixed()+' id="flowrate_data" class="form-control flowrate_data edit-vlu"></span> '+flowrate+' <br>Flowrate</td><td> <span class="value-colr"><input type="number" step="any" name="rpm_data" id="rpm_data" value='+data.rpm+' class="form-control rpm_data edit-vlu"></span> rpm<br>RPM</td></tr>'
        total_details +='<tr><td> <span class="value-colr">'+(data.bit_depth*3.281).toFixed()+'</span> '+depth+'<br>Bit Depth</td><td><span class="value-colr">'+(data.rop*3.281).toFixed(2)+'</span>'+rop+'<br>ROP</td></tr>'
    }
    $('#total_details').html(total_details)

    var rheogram_mudparameter=""
    rheogram_mudparameter +='<table class="rmp-tbl">'
    rheogram_mudparameter +='<h4 class="rmp-txt">Rheology and Mud Parameters</h4>'
    if(data.unit == 'API'){
        rheogram_mudparameter +='<tr><th>Mud Weight</th><td>'+(data.mudweight/8.345).toFixed(2)+'('+mud_weight+')</td></tr>'
        rheogram_mudparameter +='<tr><th>Rheology</th><td>'+data.selected_model+'</td></tr>'
        rheogram_mudparameter +='<tr><th>PV / YP</th><td>'+(data.pv/1000).toFixed(2)+'('+viscocity+') / '+(data.yp/0.4788).toFixed(2)+'('+yeildpoint+')</td></tr>'
        rheogram_mudparameter +='<tr><th>n/K</th><td>'+(data.n).toFixed(2)+' / '+(data.K).toFixed(2)+'</td></tr>'
    }
    else{
        rheogram_mudparameter +='<tr><th>Mud Weight</th><td>'+(data.mudweight*8.345).toFixed(2)+'('+mud_weight+')</td></tr>'
        rheogram_mudparameter +='<tr><th>Rheology</th><td>'+data.selected_model+'</td></tr>'
        rheogram_mudparameter +='<tr><th>PV / YP</th><td>'+(data.pv*1000).toFixed(2)+'('+viscocity+') / '+(data.yp*0.4788).toFixed(2)+'('+yeildpoint+')</td></tr>'
        rheogram_mudparameter +='<tr><th>n/K</th><td>'+(data.n).toFixed(2)+' / '+(data.K).toFixed(2)+'</td></tr>'
    }
    rheogram_mudparameter +='</table>'
    $('#rheogram_mudparameter').html(rheogram_mudparameter)
    if (data.unit=='API'){
        allnewtonion_pressureloss=data.allnewtonion_pressureloss*6.894757
        allbingham_pressureloss=data.allbingham_pressureloss*6.894757
        allpowerlaw_pressureloss=data.allpowerlaw_pressureloss*6.894757
        allhershel_pressureloss=data.allhershel_pressureloss*6.894757
        ty=data.ty
        allmodel_charts(Math.round(allnewtonion_pressureloss),Math.round(allbingham_pressureloss),Math.round(allpowerlaw_pressureloss),Math.round(allhershel_pressureloss),pressure)
    }
    else{
        allnewtonion_pressureloss=data.allnewtonion_pressureloss/6.894757
        allbingham_pressureloss=data.allbingham_pressureloss/6.894757
        allpowerlaw_pressureloss=data.allpowerlaw_pressureloss/6.894757
        allhershel_pressureloss=data.allhershel_pressureloss/6.894757
        ty=data.ty
        allmodel_charts(Math.round(allnewtonion_pressureloss),Math.round(allbingham_pressureloss),Math.round(allpowerlaw_pressureloss),Math.round(allhershel_pressureloss),pressure)
    }

    // console.log("unit_changef"+data)
    console.log(JSON.stringify(data));
 

    var all_surface=""
    all_surface +="<div class='card p-3'><table class='table surface-tbl'><thead><tr><th>Element</th><th>ID</th><th>Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th>"
        if(data.ty>0){
            all_surface +="<th class='hershel-clr'>Hershel</th></tr>"
        }else{
            all_surface +="</tr>"
        }
        all_surface +="<tr><th></th><th></th><th></th><th id='surface_bingham'></th><th id='surface_powerlaw'></th>"
        if(data.ty>0){
            all_surface +="<th id='surface_hershel'></th></tr></thead><tbody>"
        }else{
            all_surface +="</tr></thead><tbody>"
        }
        for(var i=0;i<data.bingham_surface_losses.length;i++){
        all_surface +='<tr>';
        if (data.unit=='API'){
            all_surface +='<td>'+data.bingham_surface_losses[i].type+'</td>';
            all_surface +='<td>'+(data.bingham_surface_losses[i].id/0.03937008).toFixed(2)+diameter+'</td>';
            all_surface +='<td>'+(data.bingham_surface_losses[i].length/3.281).toFixed(2)+length+'</td>';
            all_surface +='<td>'+Math.round(data.bingham_surface_losses[i].pressureloss/6.894757)+pressure+'</td>';
            all_surface +='<td>'+Math.round(data.powerlaw_surface_losses[i].pressureloss/6.894757)+pressure+'</td>';
            if(data.ty>0){
                all_surface +='<td>'+Math.round(data.hershel_surface_losses[i].pressureloss/6.894757)+pressure+'</td>';
            }
            // total_surface_newtonian += data.allmodalsurface[i].newtonion/6.894757
            total_surface_bingham += data.bingham_surface_losses[i].pressureloss/6.894757
            total_surface_powerlaw += data.powerlaw_surface_losses[i].pressureloss/6.894757
            total_surface_hershel += data.hershel_surface_losses[i].pressureloss/6.894757   
        }
        else{
            all_surface +='<td>'+data.bingham_surface_losses[i].type+'</td>';
            all_surface +='<td>'+(data.bingham_surface_losses[i].id*0.03937008).toFixed(2)+diameter+' </td>';
            all_surface +='<td>'+(data.bingham_surface_losses[i].length*3.281).toFixed(2)+length+'</td>';
            all_surface +='<td>'+Math.round(data.bingham_surface_losses[i].pressureloss*6.894757)+pressure+'</td>';
            all_surface +='<td>'+Math.round(data.powerlaw_surface_losses[i].pressureloss*6.894757)+pressure+'</td>';
            if(data.ty>0){
                all_surface +='<td>'+Math.round(data.hershel_surface_losses[i].pressureloss*6.894757)+pressure+'</td>';
            }
            // total_surface_newtonian += data.allmodalsurface[i].newtonion*6.894757
            total_surface_bingham += data.bingham_surface_losses[i].pressureloss*6.894757
            total_surface_powerlaw += data.powerlaw_surface_losses[i].pressureloss*6.894757
            total_surface_hershel += data.hershel_surface_losses[i].pressureloss*6.894757
        }
        all_surface +='</tr>'  

    }
    all_surface +='</tbody></table>';
    $('#allsurface-loss').html(all_surface)
    $('#surface_bingham').html(total_surface_bingham.toFixed()+pressure)
    $('#surface_powerlaw').html(total_surface_powerlaw.toFixed()+pressure)
    $('#surface_hershel').html(total_surface_hershel.toFixed()+pressure)
   
    var all_drillstring_losses = ''
    all_drillstring_losses +="<table class='table drilling-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th>"
        if(data.ty>0){
            all_drillstring_losses +="<th class='hershel-clr'>Hershel</th></tr>"
        }else{
            all_drillstring_losses +="</tr>"
        }
        all_drillstring_losses +="<tr><th></th><th></th><th></th><th class='drill-name' id='drill_bingham'></th><th class='drill-name' id='drill_powerlaw'></th>"
        if(data.ty>0){
            all_drillstring_losses +="<th class='drill-name' id='drill_hershel'></th></tr></thead><tbody>"
        }else{
            all_drillstring_losses +="</tr></thead><tbody>"
        }
        for(var i=data.bingham_drillannulur_losses.length-1;i>=0;i--){
        all_drillstring_losses +='<tr>';
        all_drillstring_losses +='<td><span class='+data.bingham_drillannulur_losses[i].element_type+'>'+data.bingham_drillannulur_losses[i].element_type+'</span></td>';
        all_drillstring_losses +='<td>'+data.bingham_drillannulur_losses[i].element+'</td>';
        if (data.unit=='API'){
            all_drillstring_losses +='<td>'+(data.bingham_drillannulur_losses[i].od/0.03937008).toFixed(2)+diameter+'/ '+(data.bingham_drillannulur_losses[i].id/0.03937008).toFixed(2)+diameter+'/'+(data.bingham_drillannulur_losses[i].length_against/3.281).toFixed()+length+'</td>';
            all_drillstring_losses +='<td>'+(data.bingham_drillannulur_losses[i].drillstringloss/6.894757).toFixed()+pressure+'</td>';
            all_drillstring_losses +='<td>'+(data.powerlaw_drillannulur_losses[i].drillstringloss/6.894757).toFixed()+pressure+'</td>';
            if(data.ty>0){
                all_drillstring_losses +='<td>'+(data.hershel_drillannulur_losses[i].drillstringloss/6.894757).toFixed()+pressure+'</td>';
            }
            all_drillstring_losses +='</tr>'
            // totaldrillstring_newtonian += data.alldrillstringloss[i].newtonion/6.894757
            totaldrillstring_bingham += data.bingham_drillannulur_losses[i].drillstringloss/6.894757
            totaldrillstring_powerlaw += data.powerlaw_drillannulur_losses[i].drillstringloss/6.894757
            totaldrillstring_hershel += data.hershel_drillannulur_losses[i].drillstringloss/6.894757
        }
        else{
            all_drillstring_losses +='<td>'+(data.bingham_drillannulur_losses[i].od*0.03937008).toFixed(2)+diameter+'/ '+(data.bingham_drillannulur_losses[i].id*0.03937008).toFixed(2)+diameter+'/ '+(data.bingham_drillannulur_losses[i].length_against*3.281).toFixed()+length+'</td>';
            all_drillstring_losses +='<td>'+(data.bingham_drillannulur_losses[i].drillstringloss*6.894757).toFixed()+pressure+'</td>';
            all_drillstring_losses +='<td>'+(data.powerlaw_drillannulur_losses[i].drillstringloss*6.894757).toFixed()+pressure+'</td>';
            if(data.ty>0){
                all_drillstring_losses +='<td>'+(data.hershel_drillannulur_losses[i].drillstringloss*6.894757).toFixed()+pressure+'</td>';
            }
            all_drillstring_losses +='</tr>'
            // totaldrillstring_newtonian += data.alldrillstringloss[i].newtonion*6.894757
            totaldrillstring_bingham += data.bingham_drillannulur_losses[i].drillstringloss*6.894757
            totaldrillstring_powerlaw += data.powerlaw_drillannulur_losses[i].drillstringloss*6.894757
            totaldrillstring_hershel += data.hershel_drillannulur_losses[i].drillstringloss*6.894757
        }
    }
    all_drillstring_losses +='</tbody></table>';
    
    $('#allpipe-loss').html(all_drillstring_losses)
    if(data.unit == 'API'){
        $('#drill_bingham').html(totaldrillstring_bingham.toFixed()+pressure)
        $('#drill_powerlaw').html(totaldrillstring_powerlaw.toFixed()+pressure)
        $('#drill_hershel').html(totaldrillstring_hershel.toFixed()+pressure)
    }else{
        $('#drill_bingham').html(totaldrillstring_bingham.toFixed()+pressure)
        $('#drill_powerlaw').html(totaldrillstring_powerlaw.toFixed()+pressure)
        $('#drill_hershel').html(totaldrillstring_hershel.toFixed()+pressure)
    }
    
    var allannularlosses=''
        cumulative_length=0
        allannularlosses +="<table class='table annuls-tbl'><thead><tr><th></th><th>BHA Element</th><th>OD / ID / Length</th><th>Cumulative Length</th><th class='bing-clr'>Bingham</th><th class='power-clr'>Powerlaw</th>"
        if(data.ty>0){
            allannularlosses +="<th class='hershel-clr'>Hershel</th></tr>"
        }else{
            allannularlosses +="</tr>"
        }
        allannularlosses +="<tr><th></th><th></th><th></th><th></th><th id='annul_bingham'></th><th id='annul_powerlaw'></th>"
        if(data.ty>0){
            allannularlosses +="<th id='annul_hershel'></th></tr></thead><tbody>"
        }else{
            allannularlosses +="</tr></thead><tbody>"
        }
        for(var i=data.bingham_drillannulur_losses.length-1;i>=0;i--){
        cumulative_length=cumulative_length+data.bingham_drillannulur_losses[i].length
        allannularlosses +='<tr>';
        if (data.unit == 'API'){
            allannularlosses +='<td><span class='+data.bingham_drillannulur_losses[i].element_type+'>'+data.bingham_drillannulur_losses[i].element_type+'</span></td>';
            allannularlosses +='<td>'+data.bingham_drillannulur_losses[i].element+'</td>';
            allannularlosses +='<td>'+(data.bingham_drillannulur_losses[i].od/0.03937008).toFixed()+diameter+' / '+(data.bingham_drillannulur_losses[i].id/0.03937008).toFixed()+diameter+' / '+(data.bingham_drillannulur_losses[i].length_against/3.281).toFixed(0)+length+'</td>';
            allannularlosses +='<td>'+(cumulative_length/3.281).toFixed(0)+length+'</td>';
            allannularlosses +='<td>'+(data.bingham_drillannulur_losses[i].pressureloss/6.894757).toFixed()+pressure+' </td>';
            allannularlosses +='<td>'+(data.powerlaw_drillannulur_losses[i].pressureloss/6.894757).toFixed()+pressure+' </td>';
            if(data.ty>0){
                allannularlosses +='<td>'+(data.hershel_drillannulur_losses[i].pressureloss/6.894757).toFixed()+pressure+' </td>';
            }
            allannularlosses +='</tr>'

            // totalannular_newtonian_loss +=   data.all_annular_pressure_loss[i].newtonion/6.894757
            totalannular_bingham_loss += data.bingham_drillannulur_losses[i].pressureloss/6.894757
            totalannular_powerlaw_loss += data.powerlaw_drillannulur_losses[i].pressureloss/6.894757
            totalannular_hershel_loss +=  data.hershel_drillannulur_losses[i].pressureloss/6.894757
        }else{
            allannularlosses +='<td><span class='+data.bingham_drillannulur_losses[i].element_type+'>'+data.bingham_drillannulur_losses[i].element_type+'</span></td>';
            allannularlosses +='<td>'+data.bingham_drillannulur_losses[i].element+'</td>';
            allannularlosses +='<td>'+(data.bingham_drillannulur_losses[i].od*0.03937008).toFixed()+diameter+'  / '+(data.bingham_drillannulur_losses[i].id*0.03937008).toFixed()+diameter+'  / '+(data.bingham_drillannulur_losses[i].length_against*3.281).toFixed(0)+length+'</td>';
            allannularlosses +='<td>'+(cumulative_length*3.281).toFixed(0)+length+'</td>';
            allannularlosses +='<td>'+(data.bingham_drillannulur_losses[i].pressureloss*6.894757).toFixed()+pressure+'</td>';
            allannularlosses +='<td>'+(data.powerlaw_drillannulur_losses[i].pressureloss*6.894757).toFixed()+pressure+'</td>';
            if(data.ty>0){
                allannularlosses +='<td>'+(data.hershel_drillannulur_losses[i].pressureloss*6.894757).toFixed()+pressure+'</td>';
            }
            allannularlosses +='</tr>'

            // totalannular_newtonian_loss += data.all_annular_pressure_loss[i].newtonion*6.894757
            totalannular_bingham_loss += data.bingham_drillannulur_losses[i].pressureloss*6.894757
            totalannular_powerlaw_loss += data.powerlaw_drillannulur_losses[i].pressureloss*6.894757
            totalannular_hershel_loss += data.hershel_drillannulur_losses[i].pressureloss*6.894757
        }
        
    }
    allannularlosses +='</tbody></table>';
    $('#allAnnular-loss').html(allannularlosses);
    $('#annul_bingham').html(totalannular_bingham_loss.toFixed()+pressure);
    $('#annul_powerlaw').html(totalannular_powerlaw_loss.toFixed()+pressure);
    $('#annul_hershel').html(totalannular_hershel_loss.toFixed()+pressure);
 

    var drillbit =''
    drillbit +='<h5 class="head-tlt">Bit Hydraulics</h5><div><table class="bh-tbl">'
    if (data.unit == 'API'){
        drillbit +='<tr><th>Bit Pressure Loss</th><td>'+(data.bit_losses[0].bit_pressure_loss*6.894757).toFixed()+pressure+'</td></tr>'
        drillbit +='<tr><th>Impact Force</th><td>'+(data.bit_losses[0].impact_forces/0.2248).toFixed()+impact+'</td></tr>'
        drillbit +='<tr><th>Jet Velocity</th><td>'+(data.bit_losses[0].jet_velocity/3.281).toFixed()+jetvelocity+' <sup>sup>/<sub>sec</sub></td></tr>'
        drillbit +='<tr><th>BHHP</th><td>'+(data.bit_losses[0].bhhp/1000*746).toFixed()+bhhp+'</td></tr>'
        drillbit +='<tr><th>HSI</th><td>'+(data.bit_losses[0].hsi).toFixed(2)+hsi+'</td></tr>'
        drillbit +='<tr><th>TFA</th><td>'+(data.bit_losses[0].tfa_value*634.09).toFixed(2)+tfa+'</td></tr>'
        drillbit +='<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse">Nozzle Details</a></td></table>';
        drillbit +=`<div class="block collapse first"><div class="block__content" id='nozzles-detail'></div></div>`
        $('#drill-bit').html(drillbit)
        var drillbit_nozzle=""
        drillbit_nozzle +='<table class="table noz-tbl"><thead><tr><th>Nozzle Size('+nozzlesize+')</th></thead><tbody>';
        for(var i=0;i<data.bit_losses.length;i++){
        for(var j=0;j<data.bit_losses[i].nozzle_size.length;j++){
            drillbit_nozzle +='<tr>';
            drillbit_nozzle +='<td>'+data.bit_losses[i].nozzle_size[j]+'</td>';
            drillbit_nozzle +='</tr>';
        }}
        drillbit_nozzle +='</tbody></table></div>';
        $('#nozzles-detail').html(drillbit_nozzle)
        totalannular.push(Math.round(data.binghamannular*6.894757),Math.round(data.powerlawannular*6.894757),Math.round(data.hershelannular*6.894757))
        totaldrillstring.push(Math.round(data.binghamdrillstring*6.894757),Math.round(data.powerlawdrillstring*6.894757),Math.round(data.hersheldrillstring*6.894757))
        drillstring_annulars(totalannular,totaldrillstring,pressure)
    }
    else{
        drillbit +='<tr><th>Bit Pressure Loss</th><td>'+(data.bit_losses[0].bit_pressure_loss/6.894757).toFixed()+pressure+'</td></tr>'
        drillbit +='<tr><th>Impact Force</th><td>'+(data.bit_losses[0].impact_forces*0.2248).toFixed()+impact+'</td></tr>'
        drillbit +='<tr><th>Jet Velocity</th><td>'+(data.bit_losses[0].jet_velocity*3.281).toFixed()+jetvelocity+'</td></tr>'
        drillbit +='<tr><th>BHHP</th><td>'+(data.bit_losses[0].bhhp*1000/746).toFixed()+bhhp+'</td></tr>'
        drillbit +='<tr><th>HSI</th><td>'+(data.bit_losses[0].hsi).toFixed(2)+hsi+'</td></tr>'
        drillbit +='<tr><th>TFA</th><td>'+(data.bit_losses[0].tfa_value/634.09).toFixed(2)+tfa+'</td></tr>'
        drillbit +='<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse">Nozzle Details</a></td></table>';
        drillbit +=`<div class="block collapse first"><div class="block__content" id='nozzles-detail'></div></div>`
        $('#drill-bit').html(drillbit)
        var drillbit_nozzle=""
        drillbit_nozzle +='<table class="table noz-tbl"><thead><tr><th>Nozzle Size('+nozzlesize+')</th></thead><tbody>';
        for(var i=0;i<data.bit_losses.length;i++){
        for(var j=0;j<data.bit_losses[i].nozzle_size.length;j++){
            drillbit_nozzle +='<tr>';
            drillbit_nozzle +='<td>'+data.bit_losses[i].nozzle_size[j]+'</td>';
            drillbit_nozzle +='</tr>';
        }}
        drillbit_nozzle +='</tbody></table></div>';
        $('#nozzles-detail').html(drillbit_nozzle)
        
        console.log(data)
        totalannular.push(Math.round(data.binghamannular/6.894757),Math.round(data.powerlawannular/6.894757),Math.round(data.hershelannular/6.894757))
        totaldrillstring.push(Math.round(data.binghamdrillstring/6.894757),Math.round(data.powerlawdrillstring/6.894757),Math.round(data.hersheldrillstring/6.894757))
       
       
        drillstring_annulars(totalannular,totaldrillstring,pressure)

    }

        


}
function allmodel_charts(totalall_newtonium,totalall_bingham,totalall_powerlaw,totalall_hershel,unit){
    allmodalchart=Highcharts.chart('allmodel_chart', {
        chart: {
            type: 'column',
            style: {
                fontFamily: 'serif',
                color:'red'
            }
        },
        title: {
            text: ''
        },
        xAxis: {
            // categories: ['Newtonian', 'Bingham Plastic', 'Power Law', 'Hershel Bulkley']
            categories: ['Bingham Plastic', 'Power Law', 'Hershel Bulkley']

        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            },
            stackLabels: {
                enabled: true,
                formatter: function () {
                return this.total+unit;      
            },
                style:{
                    color:'gray'
                }
                // style: {
                //     fontWeight: 'bold',
                //     color: ( // theme
                //         Highcharts.defaultOptions.title.style &&
                //         Highcharts.defaultOptions.title.style.color
                //     ) || 'gray'
                // }
            },
            labels: {
                formatter: function () {
                    return this.value +unit;
                }
            },
        },
        legend: {
            align: 'right',
            enabled: false,
        },
        credits: {
        enabled: false
       },
        tooltip: {
        
        },
        plotOptions: {
            series: {
            borderRadius: 5
        },

            column: {
                stacking: 'normal',
                pointWidth:30,
                // dataLabels: {
                //     enabled: true
                // }
            }
        },
        series: [{
            name: '',
            data: [
            // {
            //     y:totalall_newtonium,
            //     color: {
            // linearGradient: {
            //         x1: 0,
            //         x2: 0,
            //         y1: 1,
            //         y2: 0
            //         },
            //         stops: [
            //         [0, '#347EFC '],
            //         [1, '#43B1FE']
            //         ]
            //     },
            //  },
             {
                 y: totalall_bingham,
                 color: {
                    linearGradient: {
                            x1: 0,
                            x2: 0,
                            y1: 1,
                            y2: 0
                            },
                            stops: [
                            [0, '#1AB099 '],
                            [1, '#28DFC2']
                            ]
                        },
              },{
                y:totalall_powerlaw,
                color: {
                    linearGradient: {
                            x1: 0,
                            x2: 0,
                            y1: 1,
                            y2: 0
                            },
                            stops: [
                            [0, '#1D8B38 '],
                            [1, '#45DA6A']
                            ]
                        },
              },{
               y: totalall_hershel, 
               color: {
                    linearGradient: {
                            x1: 0,
                            x2: 0,
                            y1: 1,
                            y2: 0
                            },
                            stops: [
                            [0, '#FAD169 '],
                            [1, '#FCE766']
                            ]
                        },
            } ] ,
            
        }]
    });
   
}
function drillstring_annulars(totalannular,totaldrillstring,unit){
    Highcharts.chart('drillstring_annular', {
        chart: {
            type: 'bar',
            width: 400,
            height: 350
        },
        title: {
            text: 'Drillstring and Annular losses'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            // categories: ['N', 'BP', 'PL', 'HB'],
            categories: ['BP', 'PL', 'HB'],

            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '',
                align: 'high'
            },
            labels: {
                formatter: function () {
                    return this.value +unit;
                }
            }
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                pointWidth:5,
                dataLabels: {
                    enabled: true,
                    format: '{y} '+unit,
                    style:{
                        color:'gray'
                    }
                }
            }
        },
        legend: {
            // layout: 'vertical',
            // align: 'right',
            // verticalAlign: 'top',
            // x: -40,
            // y: 80,
            // floating: true,
            // borderWidth: 1,
            // backgroundColor:
            //     Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
            // shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Drillstring',
            data: totaldrillstring,
            color: {
            linearGradient: {
                    x1: 0,
                    x2: 0,
                    y1: 1,
                    y2: 0
                    },
                    stops: [
                    [0, '#3EA1B8'],
                    [1, '#6BE5F2']
                    ]
                }

        }, {
            name: 'Annulus',
            data: totalannular,
            color: {
            linearGradient: {
                    x1: 0,
                    x2: 0,
                    y1: 1,
                    y2: 0
                    },
                    stops: [
                    [0, '#944ED3 '],
                    [1, '#BC85FD']
                    ]
                }
        }]
    });
}

function isSeriesExists(seriesName,chart) {
    const series = chart.series;
    for (let i = 0; i < series.length; i++) {
      if (series[i].name === seriesName) {
        return true;
      }
    }
    return false;
}
