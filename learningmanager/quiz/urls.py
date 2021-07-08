from .views import (
    QuizListView,
    CategoriesListView,
    ViewQuizListByCategory,
    QuizUserProgressView,
    QuizMarkingList,
    QuizMarkingDetail,
    QuizDetailView,
    QuizTake
)
from django.urls import re_path

app_name = 'quiz'

urlpatterns = [
    re_path(r'^quizzes/$', QuizListView.as_view(), name='quiz_index'),

    re_path(
        r'^category/$',
        CategoriesListView.as_view(), name='quiz_category_list_all'
    ),
    re_path(
        r'^category/(?P<category_name>[\w|\W-]+)/$',
        ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'
    ),

    re_path(
        r'^progress/$', QuizUserProgressView.as_view(), name='quiz_progress'),
    re_path(
        r'^marking/$', QuizMarkingList.as_view(), name='quiz_marking'),
    re_path(
        r'^marking/(?P<pk>[\d.]+)/$',
        QuizMarkingDetail.as_view(), name='quiz_marking_detail'
    ),
    re_path(
        r'^(?P<slug>[\w-]+)/$',
        QuizDetailView.as_view(), name='quiz_start_page'
    ),
    re_path(
        r'^(?P<quiz_name>[\w-]+)/take/$', QuizTake.as_view(), name='quiz_question'
    ),
]
