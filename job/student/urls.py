from django.urls import path
from .import views
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, Findjob, Jobdetail, Filter, update, \
    SearchResultView, create, employer_list, updatee, deletee, notlist, notdetail, notdelete, detailss, add_review, \
    my_detail, my_reviews, delete_review, my_view, cart_count, SearchCompanyView, get_suggestions \

urlpatterns = [
    path("",views.welcome,name='welcome'),
    path("homepage/",views.homepage,name='homepage'),
    path("signup/",views.signup,name='signup'),
    path("verify_otp/",views.verify_otp,name='verify_otp'),

    path("signin/", views.login_view, name='signin'),
    path("signout/", views.signout, name='signout'),
    path('profile/',TaskList.as_view(),name='profile'),
    path('profile-create/',TaskCreate.as_view(),name='profile-create'),
    path('profile-update/<int:pk>/',TaskUpdate.as_view(),name='profile-update'),
    path('profile-delete/<int:pk>/',TaskDelete.as_view(),name='profile-delete'),
    path("findjob/", Findjob.as_view(), name='findjob'),
    path("jobdetail/<int:pk>/", Jobdetail.as_view(), name='jobdetail'),
    path('search/',SearchResultView.as_view(),name='search'),
    path('filter/',Filter.as_view(),name='filter'),
path("update<int:pk>/",update.as_view() , name='update'),
# path("applied/",Applied.as_view() , name='applied'),

#############
    path('list/',employer_list.as_view(),name='list'),
    path('employer-create/',create.as_view(),name='employer-create'),
    path('employer-update/<int:pk>/', updatee.as_view(),name='employer-update'),
    path('employer-delete/<int:pk>/',deletee.as_view(),name='employer-delete'),
path('employer-detail/<int:pk>/',detailss.as_view(),name='employer-detail'),
##############
path('notlist/',notlist.as_view(),name='notlist'),
path('notdetail/<int:pk>/',notdetail.as_view(),name='notdetail'),
path('notdelete/<int:pk>/',notdelete.as_view(),name='notdelete'),
 ##########
# path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/', views.cart, name='cart'),
# path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
path('settings/', views.settings, name='settings'),

#################
path('product/<int:pk>/', add_review, name='add_review'),

path('my_reviews/', my_reviews, name='my_reviews'),

path('delete/<int:review_id>/', delete_review, name='delete_review'),
    ####################
path('my_detail/<int:pk>/', my_detail, name='my_detail'),

########### count
path('my_view/', my_view, name='my_view'),
path('cart/count', cart_count, name='cart_count'),


    ########### save job
path('add_to_save/<int:saved_id>/', views.add_to_save, name='add_to_save'),
    path('save/', views.save, name='save'),
path('remove_from_save/<int:save_id>/', views.remove_from_save, name='remove_from_save'),
    ########### delete account
path('delete_account/', views.delete_account, name='delete_account'),

    ############## about careerbuddy
path('about/', views.about, name='about'),

############## companies

path('company/',SearchCompanyView.as_view(),name='company'),
    ##########suggessions
    path('get-suggestions/', get_suggestions, name='get-suggestions'),
]







