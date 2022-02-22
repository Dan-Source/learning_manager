from django.urls import path
from django.views.decorators.cache import cache_page
from .views import StudentCourseDetailView, StudentCourseListView, StudentEnrollCourseView


app_name = 'students'
urlpatterns = [
    path(
        'enroll-course/',
        StudentEnrollCourseView.as_view(), name='student_enroll_course'
    ),
    path(
        'courses/',
        StudentCourseListView.as_view(), name='student_course_list'
    ),
    path(
        'course/<pk>/',
        cache_page(0)(StudentCourseDetailView.as_view()),
        name='student_course_detail'
    ),
    path(
        'course/<pk>/<module_id>/',
        cache_page(0)(StudentCourseDetailView.as_view()),
        name='student_course_detail_module'),
]
