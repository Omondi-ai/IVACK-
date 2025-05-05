from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assessment, Result
from .forms import AssessmentForm, ResultForm, BulkResultUploadForm
from accounts.models import User
from django.contrib import messages
import csv
from io import TextIOWrapper, StringIO
import chardet

@login_required
def assessment_list(request):
    if request.user.role == User.PROFESSOR:
        assessments = Assessment.objects.filter(course__department=request.user.department)
    else:
        assessments = Assessment.objects.filter(course__department=request.user.department)
    return render(request, 'results/assessment_list.html', {'assessments': assessments})

@login_required
def assessment_detail(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    
    if request.user.role == User.STUDENT:
        results = Result.objects.filter(assessment=assessment, student=request.user)
    else:
        results = Result.objects.filter(assessment=assessment)
    
    return render(request, 'results/assessment_detail.html', {
        'assessment': assessment,
        'results': results,
    })

@login_required
def create_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()
            messages.success(request, 'Assessment created successfully!')
            return redirect('assessment_detail', pk=assessment.pk)
    else:
        form = AssessmentForm()
    return render(request, 'results/assessment_form.html', {'form': form})

@login_required
def create_result(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, assessment=assessment)
        if form.is_valid():
            result = form.save(commit=False)
            result.assessment = assessment
            result.save()
            messages.success(request, 'Result saved successfully!')
            return redirect('assessment_detail', pk=assessment.pk)
    else:
        form = ResultForm(assessment=assessment)
    
    return render(request, 'results/result_form.html', {
        'form': form,
        'assessment': assessment
    })


@login_required
def upload_results(request):
    if request.method == 'POST':
        form = BulkResultUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                assessment = form.cleaned_data['assessment']
                uploaded_file = form.cleaned_data['file']
                
                # Detect file encoding
                raw_data = uploaded_file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                
                # Handle the file with detected encoding
                csv_file = StringIO(raw_data.decode(encoding))
                reader = csv.DictReader(csv_file)
                
                created = updated = 0
                
                for row in reader:
                    student_id = row.get('student_id')
                    score = row.get('score')
                    remarks = row.get('remarks', '')
                    
                    if student_id and score:
                        try:
                            student = User.objects.get(student_id=student_id, role=User.STUDENT)
                            result, created_flag = Result.objects.update_or_create(
                                assessment=assessment,
                                student=student,
                                defaults={'score': score, 'remarks': remarks}
                            )
                            if created_flag:
                                created += 1
                            else:
                                updated += 1
                        except User.DoesNotExist:
                            messages.warning(request, f"Student with ID {student_id} not found")
                            continue
                
                messages.success(request, f'Successfully processed {created + updated} records (Created: {created}, Updated: {updated})')
                return redirect('assessment_detail', pk=assessment.pk)
                
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
                return redirect('upload_results')
    else:
        form = BulkResultUploadForm()
    
    return render(request, 'results/upload_results.html', {'form': form})