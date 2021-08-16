from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.conf import settings
from customUser.models import User

import json

from info.models import ECGInformation, Information, DoctorConsideration

from .decorators import info_permission, ecg_permission, is_doctor

from .forms import DoctorConsiderationForm

def prepare_for_plot(ecg) :
    channels = []
    for i in range(12) :
        channels.append([])

    for signal in ecg :
        for j in range(len(channels)) :
            channels[j].append(signal[f'ch{j+1}'])

    data = {}
    for i in range(12) :
        data[f'ch{i+1}'] = channels[i]
    
    return data


@login_required
def home(request) :
    all_ecgs = ECGInformation.objects.filter(doctors__in=[request.user, ]).order_by('-created')

    not_considered_ecgs = []
    for item in all_ecgs :
        if not item.considerations.filter(doctor=request.user) :
            not_considered_ecgs.append(item)
    paginator = Paginator(not_considered_ecgs, 10)

    # paginator = Paginator(all_ecgs, 5)
    page_number = request.GET.get('page')
    ecgs = paginator.get_page(page_number)
    return render(request, 'interface/home.html', {'ecgs' : ecgs, 'doctor_pk' : request.user.pk})


@login_required
@info_permission
def patient_info(request, pk, slug) :
    info = get_object_or_404(Information, pk=pk, slug=slug)
    return render(request, 'interface/patient_information.html', {'info' : info})


@login_required
@ecg_permission
def patient_ecg(request, pk, slug) :
    ecg = get_object_or_404(ECGInformation, pk=pk, slug=slug)
    info = get_object_or_404(Information, pk=ecg.patient.pk)
    path = ecg.ecg.url.strip(settings.MEDIA_URL)
    ecg_file = json.load(default_storage.open(path))
    data = prepare_for_plot(ecg_file)
    name = ecg.patient.fullname

    return render(request, 'interface/patient_ecg.html', {'data': data, 'info': info, 'name': name})


@login_required
@is_doctor
def nurse_history(request, pk) :
    nurse = get_object_or_404(User, pk=pk).fullname
    all_ecgs= ECGInformation.objects.filter(nurse_id=pk).order_by('-created')
    paginator = Paginator(all_ecgs, 10)
    page_number = request.GET.get('page')
    ecgs = paginator.get_page(page_number)
    return render(request, 'interface/nurse_history.html', {'ecgs' : ecgs, 'owner' : nurse})

@login_required
@is_doctor
def patient_history(request, pk) :
    patient = get_object_or_404(Information, pk=pk).fullname
    all_ecgs= ECGInformation.objects.filter(patient_id=pk).order_by('-created')
    paginator = Paginator(all_ecgs, 10)
    page_number = request.GET.get('page')
    ecgs = paginator.get_page(page_number)
    return render(request, 'interface/patient_history.html', {'ecgs' : ecgs, 'owner' : patient})


# needs decorators for permission
def write_consideration(request, pk) :
    if request.method == 'POST' :
        form = DoctorConsiderationForm(request.POST)
        if form.is_valid() :
            considerations = request.POST.get('considerations')
            ecg = get_object_or_404(ECGInformation, pk=pk)
            a = DoctorConsideration.objects.create(doctor=request.user, ecg=ecg,
                                    doctor_considerations=considerations, is_considered=True)

            return redirect('interface:home')

    form = DoctorConsiderationForm()
    return render(request, 'interface/consideration_form.html', {'form':form})


# * VIEWS IN THIS PART ARE RELATED TO THE CONSIDERED ECGs

@login_required
def ecgs_considered(request) :
    all_ecgs = ECGInformation.objects.filter(doctors__in=[request.user, ]).order_by('-created')

    considered_ecgs = []
    for item in all_ecgs :
        if item.considerations.filter(doctor=request.user) :
            considered_ecgs.append(item)


    consideration_ids = [] 
    for item in considered_ecgs :
        print(item)
        consideration_ids.append(item.considerations.get(ecg=item).pk)
    
    
    # paginator = Paginator(all_ecgs, 5)
    paginator_ecgs = Paginator(considered_ecgs, 10)
    paginator_links = Paginator(consideration_ids, 10)
    page_number = request.GET.get('page')
    ecgs = paginator_ecgs.get_page(page_number)
    links_ids = paginator_links.get_page(page_number)

    data = zip(ecgs, links_ids)
    context = {'data' : data, 'doctor_pk' : request.user.pk}

    return render(request, 'interface/considered_ecgs.html', context=context)


# needs decorators for permission
# probably a slug is needed
def update_consideration(request, pk) :
    if request.method == 'POST' :
        form = DoctorConsiderationForm(request.POST)
        if form.is_valid() :
            considerations = request.POST.get('considerations')
            DoctorConsideration.objects.filter(pk=pk).update(doctor_considerations=considerations)

            return redirect('interface:considerd_ecgs')

    data = {'considerations' : DoctorConsideration.objects.get(pk=pk).doctor_considerations}
    form = DoctorConsiderationForm(initial=data)
    return render(request, 'interface/consideration_form.html', {'form':form})


