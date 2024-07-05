def pressurelosschart_pdfstyle(chart_image):
    pdf_style = '''
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 700;
            font-size:16px;
            }

        @page  {
            size: A4 portrait; /* can use also 'landscape' for orientation */
            margin-right:1cm !important;
            margin-left:1cm !important;
        }


        @page {
            margin-bottom:100px !important;
            margin-top:235px !important;

        @top-center {
            content: element(header);
            align-items: center;
            width: 97.8%;
        }


        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            width: 20% !important;
            margin-right: 0px;
            margin-top:-30px; 
            padding:20px; 
        }

        @bottom-left {
            margin-top:35px !important;
            content: element(footer);
            font-size: 5px !important;
            margin-bottom: 30px !important;
            width: 100% !important;
        }
        }
        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
            margin-top:-60px !important;
        }
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

        .head-inv-pre {
            color: #AF2B50 !important;
            font-size: 15px !important;
        }

        .inv_rec_cls {
            border-radius: 30px !important;
            margin-top: 10px;
            border: 2px solid #000;
            width: 30%;
            margin-left: 69.7%;
            margin-bottom: 20px;
        }

        .inv_rec_cls p {
            text-align: center;
            margin: 10px 10px !important;
        }

        .invoice-received {
            font-weight: 700;
        }

       .logo {
            background-image: url("data:image/png;base64,'''+chart_image+'''");
            background-repeat: no-repeat;
            background-position: center;
            width: 500px !important;
            height: 500px !important;
        }

        .company-details {
            margin: auto;
            text-align: center;
            width: 85% !important;
        }

        .company-details h4 {
            margin-bottom: 5px;
        }

        .company-details p {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin-top: 0px;
            display: inline-block;
        }

        .parent {
            justify-content: center;
            width: 100%;
            margin: auto;
        }

        .row-border {
            border: 1px solid #c7c7c7;
        }

        .bor-top {
            border-top: none !important;
        }

        .bor-bottom-none {
            border-bottom: none !important;
        }

        .bor-ryt {
            border-right: 1px solid #c7c7c7;
        }

        .row-content h4 {
            color: #AF2B50;
            font-size: 12px;
            font-weight: 700;
            word-break: break-word;
            /* width: 25%; */
            margin: 0px !important;
            padding: 8px 0px 0px;
        }

        .row-content p {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin: 0px auto !important;
            padding: 8px 0px !important;
            line-height: 1.5;
        }

        .captions {
            color: #AF2B50;
            font-size: 12px;
            font-weight: 700;
            word-break: break-word;
            padding: 8px 5px;
        }

        .red {
            color: red !important;
            font-weight: 700 !important;
        }

        .lr-bor {
            border-left: 1px solid #c7c7c7 !important;
            border-right: 1px solid #c7c7c7 !important;
        }

        .d-flex {
        display: flex;
        }

        .justify-content-center {
        justify-content: center;
        }

        .align-items-center {
        align-items: center;
        }

        .justify-content-end {
            justify-content: end;
        }

        .col-2 {

        }

        .col-6 {
            width: 50%;
        }

        .col-4 {
            width: 33.33%;
        }

        .col-10 {
            width:83.33333333%;
        }

        .col-12 {
            width: 100%;
        }

         .text-center {
            text-align: center;
        }

        /********** Approval Table **********/

        .head-inv-pre-approval {
            color: #AF2B50;
            font-size: 10px
            font-weight: 600;
            margin-top: 10px !important;
            padding-top: 10px !important;
            margin-bottom: 0px;
        }

        .approval-head {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin-bottom: 10px !important;
            margin-top: 5px;
        }

        .invoice-approval-ptag {
            color: #000;
            font-size: 10px;
            font-weight: 500;
            margin-bottom: 10px !important;
        }

        .coversheet-approval-table {
            width: 100%;
            border: 1px solid #c7c7c7;
            border-collapse: collapse;
            /*margin-top: -20px;*/
        }

        .coversheet-approval-table th {
            color: #007480;
            /* color: #AF2B50; */
            font-size: 12px;
            font-weight: 700;
            text-align: center;
            padding: 8px 5px !important;
            border: 1px solid #c7c7c7 !important;

        }

        .coversheet-approval-table td {
                    color: #000;
                    font-size: 10px;
                    font-weight: 500;
                    margin: 0px auto !important;
                    padding: 8px 5px !important;
                    border: 1px solid #c7c7c7 !important;
                    }

        /********** Approval Table **********/ 

        .side-pad {
            padding: 0px 5px;
        }

        .bottom-pad {
            padding-bottom: 10px !important;
        }

        .caption-head {
            font-size:10px !important;
            display: inline-block; 
            margin-right: 5px !important;
            font-weight: 600 !important;
        }

        .caption-value {
            font-size: 10px !important;
        }

        .split_val {
            page-break-inside: avoid;
        }
        
        '''
    return pdf_style


def hydraulics_report_pdfstyle():
    pdf_style = '''
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 700;
            font-size:16px;
        }

        @page  {
            size: A4 portrait;
            margin-right:1cm !important;
            margin-left:1cm !important;
        }
         
        @page:first {
            @top-center { content: none; }
            @bottom-center { content: none; }
        }




        @page {
            margin-bottom:100px !important;
            margin-top:235px !important;

        @top-center {
            content: element(header);
            align-items: center;
            width: 97.8%;
        }


        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            width: 20% !important;
            margin-right: 0px;
            margin-top:-30px; 
            padding:20px; 
        }

        @bottom-left {
            margin-top:35px !important;
            content: element(footer);
            font-size: 5px !important;
            margin-bottom: 30px !important;
            width: 100% !important;
        }
        }
       
        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
            margin-top:-60px !important;
        }
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

       




   
        
        

        /*** heading SA *****/
        th{
            font-size:17px;
            font-weight:700;
        }
        td{
            font-size:15px;
            font-weight:400;
            color:#626262;
        }
        .heading-title{
            font-size:24px;
            font-weight:600;
            color:#0dd0fc;
        }
      .project-tbl{
          width:100%;
        #   border:1px solid #d3d3d3;
           border-collapse: collapse;
           border-top:2px solid red;
        #    height:400px;
           border-right:none;
           border-left:none;
           border-bottom:1px solid #d3d3d3;
           vertical-align:baseline;
      }
      .projection-tbl{
       width:100%;  
       border:1px solid #d3d3d3; 
       border-collapse: collapse;
       border-top:2px solid red;
       border-right:none;
       border-left:none;
      }
      .project-tbl th{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        font-weight:600;
        font-size:15px;
        padding:10px;
      }
      .project-tbl th:last-child{
          border-right:none;
      }
       .project-tbl th:first-child{
          border-left:none;
      }
       .project-tbl td:last-child{
          border-right:none;
      }
       .project-tbl td:first-child{
          border-left:none;
      }
      .project-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
     
      .projection-tbl th, .projection-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
      .projection-tbl th{
          font-weight:600;
        font-size:15px;
      }
      .projection-tbl th:last-child{
          border-right:none;
      }
       .projection-tbl th:first-child{
          border-left:none;
      }
       .projection-tbl td:last-child{
          border-right:none;
      }
       .projection-tbl td:first-child{
          border-left:none;
      }
    
      .full-wdt{
          width:100%;
      }
      section-head{
          font-weight:600;
      }
      .flow-proper{
           font-size:18px;
            font-weight:600;
            color:black;
            text-align:center;
      }
      .box-es{
          background:#d3d3d3;
          padding:14px;
          border-radius:20px;
          margin:0px 10px;
          color:#bb1111;
      }
      .box-es span{
          color:gray;
          font-weight:400;
          padding-left:10px;
      }
      .well-phase-name{
          font-weight:500;
          font-size:15px;
      }
      .flow-table{
          width:80%;
          margin:0px auto;
      }
      .mud-table-data{
          border:1px solid #d3d3d3;
          width:100%;
         border-collapse: collapse;
      }  
      .mud-table-data th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          border-bottom:2px solid red;
          padding:10px;
          color:#7c0201;
      }
      
      .mud-table-data td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:10px;
      }
      .section-head{
          color:#bb1111;
          font-size:18px;
          font-weight:600;
          text-align:center;
          margin:4px 0px;
      }
      .section-name{
          color:#bb1111;
          font-size:20px;
          font-weight:600;
      }
      .border-bottom{
          border-bottom:1px solid gray;
      }
      .head-samll{
          color:#bb1111;
          text-align:center;
      }
      .gel-table{
          border:1px solid #37edeb;
          border-collapse: collapse;
          width:100%;
      }
      .gel-table th{
          border:1px solid #37edeb;
          border-collapse: collapse;
          background-color:#37edeb;
          color:#fff;
          padding:8px;
      }
       .gel-table td{
          border:1px solid #37edeb;
          border-collapse: collapse;
          padding:8px;
      }
      .rheogram-table{
          border:2px solid #7c0201;
          border-right:none;
          border-left:none;
           border-collapse: collapse;
           width:100%;
      }
      .rheogram-table th{
          border:1px solid #7c0201;
           border-collapse: collapse;
           padding:8px;
      }
      .rheogram-table th:last-child{
         border-right:none;
      }
       .rheogram-table th:first-child{
         border-left:none;
      }
       .rheogram-table td:last-child{
         border-right:none;
      }
       .rheogram-table td:first-child{
         border-left:none;
      }
      
    .rheogram-table td{
          border:1px solid black;
           border-collapse: collapse;
           padding:8px;
      }
      
      .rheology-table{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          width:100%;
          border-top:2px solid red;
          border-left:none;
          border-right:none;
      }
      
      .rheology-table th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
           color:#7c0201;
      }
      
      .rheology-table td{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
      }
      
      .rheology-table th:last-child{
          border-right:none;
      }
       .rheology-table th:first-child{
          border-left:none;
      }
       .rheology-table td:last-child{
          border-right:none;
      }
       .rheology-table td:first-child{
          border-left:none;
      }
      
      
      .string-table{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        width:100%;
        border-right:none;
        border-left:none;
      }
       .string-table th{
           border:1px solid #7c0201;
           padding:8px;
           border-collapse: collapse;
           color:#7c0201;
        }
       .string-table td{
           border:1px solid #d3d3d3;
           padding:8px;
           border-collapse: collapse;
       }
       .string-table th:last-child{
         border-right:none;
      }
       .string-table th:first-child{
         border-left:none;
      }
       .string-table td:last-child{
         border-right:none;
      }
       .string-table td:first-child{
         border-left:none;
      }
      
      .total-pressure-table{
          border:1px solid #7c0201;
           border-collapse: collapse;
           width:100%;
           border-left:none;
           border-right:none;
      }
       .total-pressure-table th{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
           color:#02cbf7;
      }
       .total-pressure-table td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
      }
       .total-pressure-table th:last-child{
         border-right:none;
      }
       .total-pressure-table th:first-child{
         border-left:none;
      }
       .total-pressure-table td:last-child{
         border-right:none;
      }
       .total-pressure-table td:first-child{
         border-left:none;
      }
        .main-heading{
          font-size:50px;
          font-weight:600;
          color:#f20a30;
          text-align:center;
         marin:15px 0px;
      }
      .main-head-table{
          width:100%;
      }
      .main-head-table th{
         text-transform: capitalize;
      }
        .date-format{
            color:#03bafc;
            font-weight:600;
            font-size:16px;
        }
            .project-details{
            margin-bottom:30px;
        }
        
        
        .project-details p{
            color:#4ca2c7;
            font-size:20px;
            font-weight:600;
            # background: -webkit-linear-gradient(#eee, #333);
            margin:4px 0px;
            
        }
         .wellphase-details p{
           color:#626262;
           font-size:15px;
           text-align:right;
      }
   
       .welphase-name{
          color:#626262;
          font-size:15px;
          text-align:right;
      }
            .ecd-along-table{
          border:2px solid red;
          border-collapse:collapse;
          width:90%;
          border-right:none;
          border-left:none;
          border-bottom:none;
          margin:0px auto;
      }
        .ecd-along-table th{
           border:1px solid #d3d3d3;
           padding:8px;
           color:#7c0201;
      }
      .ecd-along-table td{
           border:1px solid #d3d3d3;
           padding:8px;
      }
      .remove-border-td{
          border-right:none;
          border-left:none;
      }
      .ecd-along-table th:last-child{
         border-right:none;
      }
       .ecd-along-table th:first-child{
         border-left:none;
      }
       .ecd-along-table td:last-child{
         border-right:none;
      }
       .ecd-along-table td:first-child{
         border-left:none;
      }
       .firstpage{
          margin-bottom:150px;
      }
        '''
    return pdf_style

def totalwell_report_pdfstyle():
    pdf_style = '''
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 700;
            font-size:16px;
        }

        @page  {
            size: A4 portrait;
            margin-right:1cm !important;
            margin-left:1cm !important;
        }
         
        @page:first {
            @top-center { content: none; }
            @bottom-center { content: none; }
        }




        @page {
            margin-bottom:100px !important;
            margin-top:235px !important;

        @top-center {
            content: element(header);
            align-items: center;
            width: 97.8%;
        }


        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            width: 20% !important;
            margin-right: 0px;
            margin-top:-30px; 
            padding:20px; 
        }

        @bottom-left {
            margin-top:35px !important;
            content: element(footer);
            font-size: 5px !important;
            margin-bottom: 30px !important;
            width: 100% !important;
        }
        }
        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
            margin-top:-60px !important;
        }
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }
        
       
        
          /*** heading SA totall*****/
        
        th{
            font-size:17px;
            font-weight:700;
        }
        td{
            font-size:15px;
            font-weight:400;
            color:#626262;
        }
        
        .project-details{
            margin-bottom:30px;
        }
        
        
        .project-details p{
            color:#4ca2c7;
            font-size:20px;
            font-weight:600;
            # background: -webkit-linear-gradient(#eee, #333);
            margin:4px 0px;
            
        }
        .date-format{
            color:#03bafc;
            font-weight:600;
            font-size:16px;
        }
        .heading-title{
            font-size:24px;
            font-weight:600;
            color:#0dd0fc;
        }
      .project-tbl{
          width:100%;
        #   border:1px solid #d3d3d3;
           border-collapse: collapse;
           border-top:2px solid red;
           border-right:none;
           border-left:none;
           border-bottom:1px solid #d3d3d3;
           vertical-align:baseline;
      }
      .projection-tbl{
       width:100%;  
       border:1px solid #d3d3d3; 
       border-collapse: collapse;
       border-top:2px solid red;
       border-right:none;
       border-left:none;
      }
      .project-tbl th{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        font-weight:600;
        font-size:15px;
        padding:10px;
      }
      .project-tbl th:last-child{
          border-right:none;
      }
       .project-tbl th:first-child{
          border-left:none;
      }
       .project-tbl td:last-child{
          border-right:none;
      }
       .project-tbl td:first-child{
          border-left:none;
      }
      .project-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
     
      .projection-tbl th, .projection-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
      .projection-tbl th{
          font-weight:600;
        font-size:15px;
      }
      .projection-tbl th:last-child{
          border-right:none;
      }
       .projection-tbl th:first-child{
          border-left:none;
      }
       .projection-tbl td:last-child{
          border-right:none;
      }
       .projection-tbl td:first-child{
          border-left:none;
      }
    
      .full-wdt{
          width:100%;
      }
      section-head{
          font-weight:600;
      }
      .flow-proper{
           font-size:18px;
            font-weight:600;
            color:black;
            text-align:center;
      }
      .box-es{
          background:#d3d3d3;
          padding:14px;
          border-radius:20px;
          margin:0px 10px;
          color:#bb1111;
      }
      .box-es span{
          color:gray;
          font-weight:400;
          padding-left:10px;
      }
      .well-phase-name{
         font-size:20px;
          font-weight:600;
          text-align:center;
           color:#bb1111;
      }
      .flow-table{
          width:80%;
          margin:0px auto;
      }
      .mud-table-data{
          border:1px solid #d3d3d3;
          width:100%;
         border-collapse: collapse;
      }  
      .mud-table-data th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          border-bottom:2px solid red;
          padding:10px;
          color:#7c0201;
      }
      
      .mud-table-data td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:10px;
      }
      .section-head{
          color:#bb1111;
          font-size:18px;
          font-weight:600;
          text-align:center;
          margin:4px 0px;
      }
      .section-name{
          color:#bb1111;
          font-size:20px;
          font-weight:600;
      }
      .border-bottom{
          border-bottom:1px solid gray;
      }
      .head-samll{
          color:#bb1111;
          text-align:center;
      }
      .gel-table{
          border:1px solid #37edeb;
          border-collapse: collapse;
          width:100%;
      }
      .gel-table th{
          border:1px solid #37edeb;
          border-collapse: collapse;
          background-color:#37edeb;
          color:#fff;
          padding:8px;
      }
       .gel-table td{
          border:1px solid #37edeb;
          border-collapse: collapse;
          padding:8px;
      }
      .rheogram-table{
          border:2px solid #7c0201;
          border-right:none;
          border-left:none;
           border-collapse: collapse;
           width:100%;
      }
      .rheogram-table th{
          border:1px solid #7c0201;
           border-collapse: collapse;
           padding:8px;
      }
      .rheogram-table th:last-child{
         border-right:none;
      }
       .rheogram-table th:first-child{
         border-left:none;
      }
       .rheogram-table td:last-child{
         border-right:none;
      }
       .rheogram-table td:first-child{
         border-left:none;
      }
      
    .rheogram-table td{
          border:1px solid black;
           border-collapse: collapse;
           padding:8px;
      }
      
      .rheology-table{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          width:100%;
          border-top:2px solid red;
          border-left:none;
          border-right:none;
      }
      
      .rheology-table th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
           color:#7c0201;
      }
      
      .rheology-table td{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
      }
      
      .rheology-table th:last-child{
          border-right:none;
      }
       .rheology-table th:first-child{
          border-left:none;
      }
       .rheology-table td:last-child{
          border-right:none;
      }
       .rheology-table td:first-child{
          border-left:none;
      }
      
      
      .string-table{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        width:100%;
        border-right:none;
        border-left:none;
      }
       .string-table th{
           border:1px solid #7c0201;
           padding:8px;
           border-collapse: collapse;
           color:#7c0201;
        }
       .string-table td{
           border:1px solid #d3d3d3;
           padding:8px;
           border-collapse: collapse;
       }
       .string-table th:last-child{
         border-right:none;
      }
       .string-table th:first-child{
         border-left:none;
      }
       .string-table td:last-child{
         border-right:none;
      }
       .string-table td:first-child{
         border-left:none;
      }
      
      .total-pressure-table{
          border:1px solid #7c0201;
           border-collapse: collapse;
           width:100%;
           border-left:none;
           border-right:none;
      }
       .total-pressure-table th{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
           color:#02cbf7;
      }
       .total-pressure-table td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
      }
       .total-pressure-table th:last-child{
         border-right:none;
      }
       .total-pressure-table th:first-child{
         border-left:none;
      }
       .total-pressure-table td:last-child{
         border-right:none;
      }
       .total-pressure-table td:first-child{
         border-left:none;
      }
      .rheogram_chart img{
        #   width:300px;
        #   height:300px;
          margin:5px auto;
          
      }
      .pressurelosschart img{
        #   width:300px;
        #   height:300px;
           margin:5px auto;
           
      }
      .wellphase-details p{
           color:#626262;
           font-size:15px;
           text-align:right;
      }
      .welphase-name{
          color:#626262;
          font-size:15px;
          text-align:right;
      }
      .ecd-along-table{
          border:2px solid red;
          border-collapse:collapse;
          width:90%;
          border-right:none;
          border-left:none;
          border-bottom:none;
          margin:0px auto;
      }
      .ecd-along-table th{
           border:1px solid #d3d3d3;
           padding:8px;
           color:#7c0201;
      }
      .ecd-along-table td{
           border:1px solid #d3d3d3;
           padding:8px;
      }
      .remove-border-td{
          border-right:none;
          border-left:none;
      }
      .ecd-along-table th:last-child{
         border-right:none;
      }
       .ecd-along-table th:first-child{
         border-left:none;
      }
       .ecd-along-table td:last-child{
         border-right:none;
      }
       .ecd-along-table td:first-child{
         border-left:none;
      }
      .ecdbitdepthchart img{
        #   width:300;
        #   height:300px;
           margin:5px auto;
          
      }
      .ecdalongwell_chart img{
        #   width:300;
        #   height:300px;
           margin:5px auto;
          
           
      }
      
      .space-top{
          margin-top:8px;
      }
      
      .main-heading{
          font-size:50px;
          font-weight:600;
          color:#f20a30;
          text-align:center;
         marin:15px 0px;
      }
      .main-head-table{
          width:100%;
      }
      .main-head-table th{
         text-transform: capitalize;
      }
       .firstpage{
          margin-bottom:150px;
      }
    '''
    return pdf_style

def sensitivity_report_pdfstyle():
    pdf_style = '''
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 700;
            font-size:16px;
        }

        @page  {
            size: A4 portrait;
            margin-right:1cm !important;
            margin-left:1cm !important;
        }
         
        @page:first {
            @top-center { content: none; }
            @bottom-center { content: none; }
        }




        @page {
            margin-bottom:100px !important;
            margin-top:235px !important;

        @top-center {
            content: element(header);
            align-items: center;
            width: 97.8%;
        }


        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            width: 20% !important;
            margin-right: 0px;
            margin-top:-30px; 
            padding:20px; 
        }

        @bottom-left {
            margin-top:35px !important;
            content: element(footer);
            font-size: 5px !important;
            margin-bottom: 30px !important;
            width: 100% !important;
        }
        }
        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
            margin-top:-60px !important;
        }
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

       




   
        
        

        /*** heading SA *****/
        th{
            font-size:17px;
            font-weight:700;
        }
        td{
            font-size:15px;
            font-weight:400;
            color:#626262;
        }
        .heading-title{
            font-size:24px;
            font-weight:600;
            color:#0dd0fc;
        }
      .project-tbl{
          width:100%;
        #   border:1px solid #d3d3d3;
           border-collapse: collapse;
           border-top:2px solid red;
        #    height:400px;
           border-right:none;
           border-left:none;
           border-bottom:1px solid #d3d3d3;
           vertical-align:baseline;
      }
      .projection-tbl{
       width:100%;  
       border:1px solid #d3d3d3; 
       border-collapse: collapse;
       border-top:2px solid red;
    #  height:400px;
       border-right:none;
       border-left:none;
      }
      .project-tbl th{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        font-weight:600;
        font-size:15px;
        padding:10px;
      }
      .project-tbl th:last-child{
          border-right:none;
      }
       .project-tbl th:first-child{
          border-left:none;
      }
       .project-tbl td:last-child{
          border-right:none;
      }
       .project-tbl td:first-child{
          border-left:none;
      }
      .project-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
     
      .projection-tbl th, .projection-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
      .projection-tbl th{
          font-weight:600;
        font-size:15px;
      }
      .projection-tbl th:last-child{
          border-right:none;
      }
       .projection-tbl th:first-child{
          border-left:none;
      }
       .projection-tbl td:last-child{
          border-right:none;
      }
       .projection-tbl td:first-child{
          border-left:none;
      }
    
      .full-wdt{
          width:100%;
      }
      section-head{
          font-weight:600;
      }
      .flow-proper{
           font-size:18px;
            font-weight:600;
            color:black;
            text-align:center;
      }
      .box-es{
          background:#d3d3d3;
          padding:14px;
          border-radius:20px;
          margin:0px 10px;
          color:#bb1111;
      }
      .box-es span{
          color:gray;
          font-weight:400;
          padding-left:10px;
      }
      .well-phase-name{
          font-weight:500;
          font-size:15px;
      }
      .flow-table{
          width:80%;
          margin:0px auto;
      }
      .mud-table-data{
          border:1px solid #d3d3d3;
          width:100%;
         border-collapse: collapse;
      }  
      .mud-table-data th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          border-bottom:2px solid red;
          padding:10px;
          color:#7c0201;
      }
      
      .mud-table-data td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:10px;
      }
      .section-head{
          color:#bb1111;
          font-size:18px;
          font-weight:600;
          text-align:center;
          margin:4px 0px;
      }
      .section-name{
          color:#bb1111;
          font-size:20px;
          font-weight:600;
      }
      .border-bottom{
          border-bottom:1px solid gray;
      }
      .head-samll{
          color:#bb1111;
          text-align:center;
      }
      .gel-table{
          border:1px solid #37edeb;
          border-collapse: collapse;
          width:100%;
      }
      .gel-table th{
          border:1px solid #37edeb;
          border-collapse: collapse;
          background-color:#37edeb;
          color:#fff;
          padding:8px;
      }
       .gel-table td{
          border:1px solid #37edeb;
          border-collapse: collapse;
          padding:8px;
      }
      .rheogram-table{
          border:2px solid #7c0201;
          border-right:none;
          border-left:none;
           border-collapse: collapse;
           width:100%;
      }
      .rheogram-table th{
          border:1px solid #7c0201;
           border-collapse: collapse;
           padding:8px;
      }
      .rheogram-table th:last-child{
         border-right:none;
      }
       .rheogram-table th:first-child{
         border-left:none;
      }
       .rheogram-table td:last-child{
         border-right:none;
      }
       .rheogram-table td:first-child{
         border-left:none;
      }
      
    .rheogram-table td{
          border:1px solid black;
           border-collapse: collapse;
           padding:8px;
      }
      
      .rheology-table{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          width:100%;
          border-top:2px solid red;
          border-left:none;
          border-right:none;
      }
      
      .rheology-table th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
           color:#7c0201;
      }
      
      .rheology-table td{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
      }
      
      .rheology-table th:last-child{
          border-right:none;
      }
       .rheology-table th:first-child{
          border-left:none;
      }
       .rheology-table td:last-child{
          border-right:none;
      }
       .rheology-table td:first-child{
          border-left:none;
      }
      
      
      .string-table{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        width:100%;
        border-right:none;
        border-left:none;
      }
       .string-table th{
           border:1px solid #7c0201;
           padding:8px;
           border-collapse: collapse;
           color:#7c0201;
        }
       .string-table td{
           border:1px solid #d3d3d3;
           padding:8px;
           border-collapse: collapse;
       }
       .string-table th:last-child{
         border-right:none;
      }
       .string-table th:first-child{
         border-left:none;
      }
       .string-table td:last-child{
         border-right:none;
      }
       .string-table td:first-child{
         border-left:none;
      }
      
      .total-pressure-table{
          border:1px solid #7c0201;
           border-collapse: collapse;
           width:100%;
           border-left:none;
           border-right:none;
      }
       .total-pressure-table th{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
           color:#02cbf7;
      }
       .total-pressure-table td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
      }
       .total-pressure-table th:last-child{
         border-right:none;
      }
       .total-pressure-table th:first-child{
         border-left:none;
      }
       .total-pressure-table td:last-child{
         border-right:none;
      }
       .total-pressure-table td:first-child{
         border-left:none;
      }
        .main-heading{
          font-size:50px;
          font-weight:600;
          color:#f20a30;
          text-align:center;
         marin:15px 0px;
      }
      .main-head-table{
          width:100%;
      }
      .main-head-table th{
         text-transform: capitalize;
      }
        .date-format{
            color:#03bafc;
            font-weight:600;
            font-size:16px;
        }
            .project-details{
            margin-bottom:30px;
        }
        
        
        .project-details p{
            color:#4ca2c7;
            font-size:20px;
            font-weight:600;
            # background: -webkit-linear-gradient(#eee, #333);
            margin:4px 0px;
            
        }
         .wellphase-details p{
           color:#626262;
           font-size:15px;
           text-align:right;
      }
     
       .welphase-name{
          color:#626262;
          font-size:15px;
          text-align:right;
      }
            .ecd-along-table{
          border:2px solid red;
          border-collapse:collapse;
          width:90%;
          border-right:none;
          border-left:none;
          border-bottom:none;
          margin:0px auto;
      }
        .ecd-along-table th{
           border:1px solid #d3d3d3;
           padding:8px;
           color:#7c0201;
      }
      .ecd-along-table td{
           border:1px solid #d3d3d3;
           padding:8px;
      }
      .remove-border-td{
          border-right:none;
          border-left:none;
      }
      .ecd-along-table th:last-child{
         border-right:none;
      }
       .ecd-along-table th:first-child{
         border-left:none;
      }
       .ecd-along-table td:last-child{
         border-right:none;
      }
       .ecd-along-table td:first-child{
         border-left:none;
      }
      .firstpage{
          margin-bottom:150px;
      }
        '''
    return pdf_style

def totalwell_report_pdfstyle():
    pdf_style = '''
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 700;
            font-size:16px;
        }

        @page  {
            size: A4 portrait;
            margin-right:1cm !important;
            margin-left:1cm !important;
        }
         
        @page:first {
            @top-center { content: none; }
            @bottom-center { content: none; }
        }




        @page {
            margin-bottom:100px !important;
            margin-top:235px !important;

        @top-center {
            content: element(header);
            align-items: center;
            width: 97.8%;
        }


        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10px;
            width: 20% !important;
            margin-right: 0px;
            margin-top:-30px; 
            padding:20px; 
        }

        @bottom-left {
            margin-top:35px !important;
            content: element(footer);
            font-size: 5px !important;
            margin-bottom: 30px !important;
            width: 100% !important;
        }
        }
        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
            margin-top:-60px !important;
        }
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

       
        
          /*** heading SA totall*****/
        
        th{
            font-size:17px;
            font-weight:700;
        }
        td{
            font-size:15px;
            font-weight:400;
            color:#626262;
        }
        
        .project-details{
            margin-bottom:30px;
        }
        
        
        .project-details p{
            color:#4ca2c7;
            font-size:20px;
            font-weight:600;
            # background: -webkit-linear-gradient(#eee, #333);
            margin:4px 0px;
            
        }
        .date-format{
            color:#03bafc;
            font-weight:600;
            font-size:16px;
        }
        .heading-title{
            font-size:24px;
            font-weight:600;
            color:#0dd0fc;
        }
      .project-tbl{
          width:100%;
        #   border:1px solid #d3d3d3;
           border-collapse: collapse;
           border-top:2px solid red;
        #    height:400px;
           border-right:none;
           border-left:none;
           border-bottom:1px solid #d3d3d3;
           vertical-align:baseline;
      }
      .projection-tbl{
       width:100%;  
       border:1px solid #d3d3d3; 
       border-collapse: collapse;
       border-top:2px solid red;
    #    height:400px;
       border-right:none;
       border-left:none;
      }
      .project-tbl th{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        font-weight:600;
        font-size:15px;
        padding:10px;
      }
      .project-tbl th:last-child{
          border-right:none;
      }
       .project-tbl th:first-child{
          border-left:none;
      }
       .project-tbl td:last-child{
          border-right:none;
      }
       .project-tbl td:first-child{
          border-left:none;
      }
      .project-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
     
      .projection-tbl th, .projection-tbl td{
          border:1px solid #d3d3d3;
          padding:10px;
      }
      .projection-tbl th{
          font-weight:600;
        font-size:15px;
      }
      .projection-tbl th:last-child{
          border-right:none;
      }
       .projection-tbl th:first-child{
          border-left:none;
      }
       .projection-tbl td:last-child{
          border-right:none;
      }
       .projection-tbl td:first-child{
          border-left:none;
      }
    
      .full-wdt{
          width:100%;
      }
      section-head{
          font-weight:600;
      }
      .flow-proper{
           font-size:18px;
            font-weight:600;
            color:black;
            text-align:center;
      }
      .box-es{
          background:#d3d3d3;
          padding:14px;
          border-radius:20px;
          margin:0px 10px;
          color:#bb1111;
      }
      .box-es span{
          color:gray;
          font-weight:400;
          padding-left:10px;
      }
      .well-phase-name{
         font-size:20px;
          font-weight:600;
          text-align:center;
           color:#bb1111;
      }
      .flow-table{
          width:80%;
          margin:0px auto;
      }
      .mud-table-data{
          border:1px solid #d3d3d3;
          width:100%;
         border-collapse: collapse;
      }  
      .mud-table-data th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          border-bottom:2px solid red;
          padding:10px;
          color:#7c0201;
      }
      
      .mud-table-data td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:10px;
      }
      .section-head{
          color:#bb1111;
          font-size:18px;
          font-weight:600;
          text-align:center;
          margin:4px 0px;
      }
      .section-name{
          color:#bb1111;
          font-size:20px;
          font-weight:600;
      }
      .border-bottom{
          border-bottom:1px solid gray;
      }
      .head-samll{
          color:#bb1111;
          text-align:center;
      }
      .gel-table{
          border:1px solid #37edeb;
          border-collapse: collapse;
          width:100%;
      }
      .gel-table th{
          border:1px solid #37edeb;
          border-collapse: collapse;
          background-color:#37edeb;
          color:#fff;
          padding:8px;
      }
       .gel-table td{
          border:1px solid #37edeb;
          border-collapse: collapse;
          padding:8px;
      }
      .rheogram-table{
          border:2px solid #7c0201;
          border-right:none;
          border-left:none;
           border-collapse: collapse;
           width:100%;
      }
      .rheogram-table th{
          border:1px solid #7c0201;
           border-collapse: collapse;
           padding:8px;
      }
      .rheogram-table th:last-child{
         border-right:none;
      }
       .rheogram-table th:first-child{
         border-left:none;
      }
       .rheogram-table td:last-child{
         border-right:none;
      }
       .rheogram-table td:first-child{
         border-left:none;
      }
      
    .rheogram-table td{
          border:1px solid black;
           border-collapse: collapse;
           padding:8px;
      }
      
      .rheology-table{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          width:100%;
          border-top:2px solid red;
          border-left:none;
          border-right:none;
      }
      
      .rheology-table th{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
           color:#7c0201;
      }
      
      .rheology-table td{
          border:1px solid #d3d3d3;
          border-collapse: collapse;
          padding:5px;
      }
      
      .rheology-table th:last-child{
          border-right:none;
      }
       .rheology-table th:first-child{
          border-left:none;
      }
       .rheology-table td:last-child{
          border-right:none;
      }
       .rheology-table td:first-child{
          border-left:none;
      }
      
      
      .string-table{
        border:1px solid #d3d3d3;
        border-collapse: collapse;
        width:100%;
        border-right:none;
        border-left:none;
      }
       .string-table th{
           border:1px solid #7c0201;
           padding:8px;
           border-collapse: collapse;
           color:#7c0201;
        }
       .string-table td{
           border:1px solid #d3d3d3;
           padding:8px;
           border-collapse: collapse;
       }
       .string-table th:last-child{
         border-right:none;
      }
       .string-table th:first-child{
         border-left:none;
      }
       .string-table td:last-child{
         border-right:none;
      }
       .string-table td:first-child{
         border-left:none;
      }
      
      .total-pressure-table{
          border:1px solid #7c0201;
           border-collapse: collapse;
           width:100%;
           border-left:none;
           border-right:none;
      }
       .total-pressure-table th{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
           color:#02cbf7;
      }
       .total-pressure-table td{
          border:1px solid #d3d3d3;
           border-collapse: collapse;
           padding:6px;
      }
       .total-pressure-table th:last-child{
         border-right:none;
      }
       .total-pressure-table th:first-child{
         border-left:none;
      }
       .total-pressure-table td:last-child{
         border-right:none;
      }
       .total-pressure-table td:first-child{
         border-left:none;
      }
      .rheogram_chart img{
        #   width:300px;
        #   height:300px;
          margin:5px auto;
          object-fit:contain;
      }
      .pressurelosschart img{
        #   width:300px;
        #   height:300px;
           margin:5px auto;
           object-fit:contain;
      }
      .wellphase-details p{
           color:#626262;
           font-size:15px;
           text-align:right;
      }
      .welphase-name{
          color:#626262;
          font-size:15px;
          text-align:right;
      }
      .ecd-along-table{
          border:2px solid red;
          border-collapse:collapse;
          width:90%;
          border-right:none;
          border-left:none;
          border-bottom:none;
          margin:0px auto;
      }
      .ecd-along-table th{
           border:1px solid #d3d3d3;
           padding:8px;
           color:#7c0201;
      }
      .ecd-along-table td{
           border:1px solid #d3d3d3;
           padding:8px;
      }
      .remove-border-td{
          border-right:none;
          border-left:none;
      }
      .ecd-along-table th:last-child{
         border-right:none;
      }
       .ecd-along-table th:first-child{
         border-left:none;
      }
       .ecd-along-table td:last-child{
         border-right:none;
      }
       .ecd-along-table td:first-child{
         border-left:none;
      }
      .ecdbitdepthchart img{
        #   width:300;
        #   height:300px;
           margin:5px auto;
           object-fit:contain;
      }
      .ecdalongwell_chart img{
        #   width:300;
        #   height:300px;
           margin:5px auto;
           object-fit:contain;
           
      }
      
      .space-top{
          margin-top:8px;
      }
      
      .main-heading{
          font-size:50px;
          font-weight:600;
          color:#f20a30;
          text-align:center;
         marin:15px 0px;
      }
      .main-head-table{
          width:100%;
      }
      .main-head-table th{
         text-transform: capitalize;
      }
    '''
    return pdf_style