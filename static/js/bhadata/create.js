$("document").ready(function() {
    $(document.body).on("click",".drillpipe_nod > li",function () { 
        $(this).addClass('active').siblings().removeClass('active');
        var normal_od=$(this).attr('databasevalue');
        var well_id = $('#well').val();
        $.ajax({ 
           type: "GET",                      
           url: "/wells/bhadata/getweight_drillpipe",                    
           data: {
             normal_od:normal_od,
             well_id:well_id
           },
           dataType: "json",
           success: function (data) { 
                $(".drillpipe_weight li").remove();
                $('#pipe_weight_head').show();
                for(i=0;i<data.data.length;i++){
                $('.drillpipe_weight').append('<li databasevalue ="'+data.data[i].databasevalue+'" drillpipe_weight="'+data.data[i].weight +'">'+ data.data[i].weight+'</li>');
                }
                $(".drillpipe_grade li").remove(); 
                $(".drillpipe_jointtype li").remove(); 
                $(".drillpipe_jointod li").remove();  
                $(".drillpipe_class li").hide(); 
                $(".drillpipe_onejoint_length").hide(); 
                $("#pipe_grade_head").hide();
                $("#pipe_type_head").hide();
                $("#pipe_od_head").hide();
                $("#pipe_class_head").hide();
                $("#pipe_joint_head").hide();
            }
        });
    });
    $(document.body).on("click",".drillpipe_weight > li",function () { 
        $(this).addClass('active').siblings().removeClass('active');
        var drillpipe_val = $(this).attr('drillpipe_weight');
        var drillpipe_weight = $(this).attr('databasevalue');  
        if(well_type=='PLAN'){
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(drillpipe_weight);
        }else{
          $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(drillpipe_weight);
        }
        var normal_od=$('ul.drillpipe_nod').find('li.active').attr('databasevalue');
        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getgrade_drillpipe",                    
            data: {
                drillpipe_weight:drillpipe_weight,
                normal_od:normal_od
            },
            dataType: "json",
            success: function (data) { 
                $(".drillpipe_grade li").remove(); 
                $("#pipe_grade_head").show();
                for(i=0;i<data.data.length;i++){
                    $('.drillpipe_grade').append('<li drillpipe_grade="'+data.data[i].steel_grade +'">'+ data.data[i].steel_grade+'</li>');
                }
                $(".drillpipe_jointtype li").remove(); 
                $(".drillpipe_jointod li").remove(); 
                $(".drillpipe_class li").hide(); 
                $(".drillpipe_onejoint_length").hide();
                $("#pipe_type_head").hide();
                $("#pipe_od_head").hide();
                $("#pipe_class_head").hide();
                $("#pipe_joint_head").hide();
            }
        });
    });
    
    $(document.body).on("click",".drillpipe_grade > li",function () { 
        $(this).addClass('active').siblings().removeClass('active');
        var drillpipe_grade = $(this).attr('drillpipe_grade');  
        if(well_type=='PLAN'){
        $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.grade').val(drillpipe_grade);
        }
        else{
        $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.grade').val(drillpipe_grade);
    
        }
        var normal_od=$('ul.drillpipe_nod').find('li.active').attr('databasevalue');
        var drillpipe_weight=$('ul.drillpipe_weight').find('li.active').attr('databasevalue');
        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getjointtype_drillpipe",                    
            data: {
                drillpipe_weight:drillpipe_weight,
                normal_od:normal_od,
                drillpipe_grade:drillpipe_grade
            },
            dataType: "json",
            success: function (data) { 
                $(".drillpipe_jointtype li").remove(); 
                $("#pipe_type_head").show();
                for(i=0;i<data.data.length;i++){
                    $('.drillpipe_jointtype').append('<li drillpipe_jointtype="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</li>');
                }
                $(".drillpipe_class li").hide(); 
                $(".drillpipe_jointod li").remove(); 
                $(".drillpipe_onejoint_length").hide();
                $("#pipe_od_head").hide();
                $("#pipe_class_head").hide();
                $("#pipe_joint_head").hide();
            }
        });
    });

    $(document.body).on("click",".drillpipe_jointtype > li",function () { 
        $(this).addClass('active').siblings().removeClass('active');
        var drillpipe_jointtype = $(this).attr('drillpipe_jointtype');  
        if(well_type=='PLAN'){
        $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(drillpipe_jointtype);
        }else{
        $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.connection_type').val(drillpipe_jointtype);
        }
        var normal_od=$('ul.drillpipe_nod').find('li.active').attr('databasevalue')
        var nod=$('ul.drillpipe_nod').find('li.active').attr('drillpipe_nod');
        var drillpipe_weight=$('ul.drillpipe_weight').find('li.active').attr('databasevalue');
        var drillpipe_grade=$('ul.drillpipe_grade').find('li.active').attr('drillpipe_grade');
        var well_id=$('#well').val();
        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getjointod_drillpipe",                    
            data: {
                drillpipe_weight:drillpipe_weight,
                normal_od:normal_od,
                drillpipe_grade:drillpipe_grade,
                drillpipe_jointtype:drillpipe_jointtype,
                well_id:well_id,
                nod:nod,
            },
            dataType: "json",
            success: function (data) { 
                if(well_type=='PLAN'){
                $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val(data.data[0][0].data);
                $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
                $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_od').val(normal_od);
                $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id.data);
                }else{
                $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.identity').val(data.data[0][0].data);
                $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
                $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.database_od').val(normal_od);
                $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id.data);
                }
                $(".drillpipe_jointod li").remove(); 
                $("#pipe_od_head").show();
                for(i=0;i<data.data.length;i++){
                $('.drillpipe_jointod').append('<li drillpipe_jointod="'+data.data[i][1].data+'">'+ data.data[i][1].data+'</li>');
                }
                $(".drillpipe_class li").hide(); 
                $(".drillpipe_onejoint_length").hide();
                $("#pipe_class_head").hide();
                $("#pipe_joint_head").hide();
            }
        });
    });

    $(document.body).on("click",".drillpipe_jointod > li",function () { 
        $(this).addClass('active').siblings().removeClass('active');
        var drillpipe_jointod = $(this).attr('drillpipe_jointod');  
        if(well_type=='PLAN'){
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(drillpipe_jointod);
        }else{
          $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.tool_od').val(drillpipe_jointod);
        }
        var normal_od=$('ul.drillpipe_nod').find('li.active').attr('drillpipe_nod');
        var drillpipe_weight=$('ul.drillpipe_weight').find('li.active').attr('databasevalue');
        var drillpipe_grade=$('ul.drillpipe_grade').find('li.active').attr('drillpipe_grade');
        var drillpipe_jointtype=$('ul.drillpipe_jointtype').find('li.active').attr('drillpipe_jointtype');
        $(".drillpipe_class li").removeClass('active');
        $(".drillpipe_class li").show();
        $("#pipe_class_head").show();
        $(".drillpipe_onejoint_length").hide();
        $("#pipe_joint_head").hide();
        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getclass_drillpipe",                    
            data: {
                drillpipe_weight:drillpipe_weight,
                normal_od:normal_od,
                drillpipe_grade:drillpipe_grade,
                drillpipe_jointtype:drillpipe_jointtype,
                drillpipe_jointod:drillpipe_jointod
            },
            dataType: "json",
            success: function (data) { 
                $(".drillpipe_class li").remove(); 
                
                for(i=0;i<data.data.length;i++){
                $('.drillpipe_class').append('<li value="'+data.data[i].class_type +'">'+ data.data[i].class_type+'</li>');
                }
                $(".drillpipe_onejoint_length").hide();
            }
        });
    });
    $(document.body).on("click",".drillpipe_class > li",function () { 
        $(this).addClass('active').siblings().removeClass('active');
        var classtype=$(this).attr('value');
        console.log(classtype)
        if(well_type=='PLAN'){
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
        }else{
          $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
        }
        $("#pipe_joint_head").show();
        $('.drillpipe_onejoint_length').show();
    });
      
})