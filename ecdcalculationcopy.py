def ecdcalculation(holemd,holetvd,previousmd,previoustvd,mud_weight,annular_pressure_loss,well_id,request):
    # print(f"holemd {holemd}")
    # print(f"holetvd {holetvd}")
    # print(f"previousmd {previousmd}")
    # print(f"previoustvd {previoustvd}")
    allecd_data=[]
    allannular_data=[]
    totalannularloss=sum(annularloss['pressureloss'] for annularloss in annular_pressure_loss)
    totalannularloss_withoutopenhole=sum(annularloss['pressureloss'] for annularloss in annular_pressure_loss if annularloss['element_type']!="OH")
    casinglength=sum(annularloss['length_against'] for annularloss in annular_pressure_loss if annularloss['element_type']!="OH")
    revcum=0
    for annular in annular_pressure_loss:
        revcum +=annular['length_against']
        apl=annular['pressureloss']/annular['length_against']
        allannular_data.append({
            'length':annular['length_against'],
            'revcum':revcum,
            'apl':apl
        })
    step_size=100
    depth=0
    previous_depth=0
    startdepth=allannular_data[0]['revcum']
    todepth=holemd

    # print(f"todepth {todepth}")
    while depth<holemd:
        depth=depth+step_size
        if(depth<=startdepth):
            md=depth
        else:
            i=0
            while i<len(allannular_data)-1:
                remaining_element=(len(allannular_data)-1)-i
                if(remaining_element>1):
                    if(previous_depth<allannular_data[i]['revcum'] and (previous_depth+step_size)>allannular_data[i]['revcum']):
                        md=allannular_data[i]['revcum']
                        break
                    else:
                        if(depth>allannular_data[i]['revcum'] and depth<=allannular_data[i+1]['revcum']):
                           md=depth
                           break
                else:
                    if(previous_depth<allannular_data[i]['revcum'] and (previous_depth+step_size)>allannular_data[i]['revcum']):
                        md=allannular_data[i]['revcum']
                        break
                    else:
                        if(depth<=todepth and depth>allannular_data[i]['revcum']):
                           md=depth
                           break
                        else:
                            md=todepth
                            break
                i +=1
        previous_depth=depth
        # print(f"depth {depth}")
        # print(f"md {md}")

        if(md<=startdepth):
            calculatedapl=allannular_data[0]['apl']*md
        else:
            # print(f"md {md}")
            i=0
            while i<len(allannular_data):
                if(i==0):
                    if(md>allannular_data[i]['revcum'] and md<=allannular_data[i+1]['revcum']):
                        calculatedapl=(md-allannular_data[i]['revcum'])*allannular_data[i+1]['apl']+allannular_data[i]['apl']*allannular_data[i]['revcum']
                else:
                    if(md>allannular_data[i]['revcum'] and md<=allannular_data[i+1]['revcum']):
                        calculatedapl=(md-allannular_data[i]['revcum'])*allannular_data[i+1]['apl']
                        j=0
                        while j<=i:
                            calculatedapl=calculatedapl+allannular_data[j]['apl']*allannular_data[j]['length']
                            j +=1
                i +=1
        allecd_data.append({'depth':depth,'md':md,'apl':calculatedapl})
    print(f"allecd_data {allecd_data}")