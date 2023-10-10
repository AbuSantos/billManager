# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()

#             #Authenticate and login
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, "You've successfully registered!")
#             return redirect('home')
#     else:
#         form= SignUpForm()
#         return render(request, 'register.html',{'form':form})
#     return render(request, 'register.html',{'form':form})
# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()

#             # Fetch the UserProfile for the newly registered user
#             # try:
#             #     user_profile = UserProfile.objects.get(user=user)
#             # except UserProfile.DoesNotExist:
#             #     # user_profile = None
#             user_profile.objects.create(user=user)

#             # Authenticate and login
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "You've successfully registered!")

#                 # If a UserProfile exists, associate it with the user
#                 if user_profile:
#                     user_profile.user = user
#                     user_profile.save()
                    
#                 return redirect('home')
#             else:
#                 messages.error(request, "There was an error logging in, please try again...")
#         else:
#             messages.error(request, "There was an error registering your account.")
#     else:
#         form = SignUpForm()
#     return render(request, 'register.html', {'form': form})