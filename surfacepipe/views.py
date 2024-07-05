from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from surfacepipe.models import SurfacePipe,SurfacePipeData
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SurfacePipeForm,SurfacePipeDataForm
from django.views.generic import ListView, DetailView
from django.forms import formset_factory
from wells.models import Wells,WellUsers,CoordinateSystems,Projections
from surfacepipe.models import SurfaceNameModels
from custom_auth.getunit import adduserlog

# Create your views here.
def details(request,well_id):
    try:
        surfacepipe=SurfacePipe.objects.get(company=request.company,well=well_id)
    except SurfacePipe.DoesNotExist:
        surfacepipe = None
    if(surfacepipe is None):
        return redirect('surfacepipe:create',well_id=well_id)

    surfacepipedata=SurfacePipeData.objects.filter(surfacepipe=surfacepipe,status=1)
    return render(request,'surfacepipe/view.html',{'surfacepipe': surfacepipe,'surfacepipedata':surfacepipedata,'well_id':well_id})


def create(request,well_id):
    if request.method == 'POST':
        form = SurfacePipeForm(request.POST)
        if form.is_valid():
            surfacepipe=form.save()
            surfacepipe.company=request.company
            surfacepipe.save()
            names=request.POST.getlist('name')
            length=request.POST.getlist('length')
            identity=request.POST.getlist('identity')
            i = 0
            while i < len(names):
                if(names[i]):     
                    SurfacePipeData.objects.create(name=names[i],length=length[i],identity=identity[i],surfacepipe=surfacepipe,well_id=well_id,company=request.company)
                i += 1
            source_id=surfacepipe.id
            userlog=adduserlog('Surfacepipe Created',request,source_id,'Surfacepipe',request.user.licence_type)
            return redirect('surfacepipe:detail', well_id=well_id)
        else:
            print(form.errors)
    form = SurfacePipeForm()
    surface_names= SurfaceNameModels.objects.all()
    return render(request,'surfacepipe/create.html',{'form': form,'well_id':well_id,'surface_names':surface_names})


def edit(request, pk, template_name='surfacepipe/edit.html'):
    surfacepipe = get_object_or_404(SurfacePipe, pk=pk)
    form = SurfacePipeForm(request.POST or None, instance=surfacepipe)
    surfacepipedata = SurfacePipeData.objects.filter(surfacepipe=pk,status=1)
    well_id=surfacepipe.well_id
    if form.is_valid():
        surfacepipe=form.save()
        surfacepipe.company=request.company
        surfacepipe.save()
        # SurfacePipeData.objects.filter(surfacepipe=pk).delete()
        names=request.POST.getlist('name')
        length=request.POST.getlist('length')
        identity=request.POST.getlist('identity')
        surfacepipe_id=request.POST.getlist('surfacepipe_id')
        i = 0
        currentid=[]
        while i < len(names):
            if(names[i]):
                if(surfacepipe_id[i]):
                    currentid.append(surfacepipe_id[i])
                    SurfacePipeData.objects.filter(id=surfacepipe_id[i]).update(name=names[i],length=length[i],identity=identity[i])
                else:
                    SurfacePipeData.objects.create(name=names[i],length=length[i],identity=identity[i],surfacepipe=surfacepipe,well_id=well_id,company=request.company)
                    surface_id=SurfacePipeData.objects.values('id').last()
                    currentid.append(surface_id['id'])
            i += 1
        SurfacePipeData.objects.filter(well_id=well_id).exclude(id__in=currentid).update(status=0)            
        source_id=surfacepipe.id
        userlog=adduserlog('Surfacepipe Edited',request,source_id,'Surfacepipe',request.user.licence_type)
        return redirect('surfacepipe:detail',well_id=well_id)
    return render(request, template_name, {'form':form,'surfacepipedata':surfacepipedata,'well_id':well_id})



def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    surfacepipe = get_object_or_404(SurfacePipe, pk=pk)
    well_id=surfacepipe.well_id
    source_id=surfacepipe.id
    surfacepipe.delete()
    userlog=adduserlog('Surfacepipe Deleted',request,source_id,'Surfacepipe',request.user.licence_type)
    return redirect('surfacepipe:detail', well_id=well_id)



