from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .models import UserReg, DeptReg, Post, Vote, Message, Complaints, Announcement, Comments
from django.db.models.functions import Coalesce
from django.db.models import Max, Value, F
from .form import PostForm
from django.shortcuts import get_object_or_404

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta



# Create your views here.

class Home(TemplateView):
    template_name = "login.html"


class UserCreateView(CreateView):
    model = UserReg
    fields = ['fname','lname','house_name','house_number','gender','dob','username','password','email','phone_number','panchayath','district','state','country','photo']
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        max_uid = UserReg.objects.aggregate(max_uid=Coalesce(Max('uid'), Value(0)))['max_uid']
        bno = int(max_uid) + 1
        initial = super(UserCreateView, self).get_initial(**kwargs)
        initial['uid'] = bno
        # initial['right'] = 'user'
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)
        id = post.uid
        n = post.username
        print(id)
        found = 0
        if UserReg.objects.filter(username=n).exists():
            found = 1
        if found == 0:
            post.save()
            return HttpResponseRedirect('http://127.0.0.1:8000')
        else:
            return render(self.request, "UserReg_form.html")


class DepartmentCreateView(CreateView):
    model = DeptReg
    fields = ['department','username','password','email','panchayath','district','state','country','photo']
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        max_did = DeptReg.objects.aggregate(max_did=Coalesce(Max('did'), Value(0)))['max_did']
        bno = int(max_did) + 1
        initial = super(DepartmentCreateView, self).get_initial(**kwargs)
        initial['did'] = bno
        # initial['right'] = 'user'
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)
        id = post.did
        n = post.username
        print(id)
        found = 0
        if DeptReg.objects.filter(username=n).exists():
            found = 1
        if found == 0:
            post.save()
            return HttpResponseRedirect('http://127.0.0.1:8000')
        else:
            return render(self.request, "DeptReg_form.html")


class DepartmentListView(ListView):
    model = DeptReg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = DeptReg.objects.filter(status='new department')
        return context


def DepartmentApprove(request, did):
    DeptReg.objects.filter(did=did).update(status="Department")
    return redirect('/list/')


def DepartmentReject(request, did):
    DeptReg.objects.filter(did=did).update(status='Reject')
    return redirect('/list/')



def loginpage(request):
    if request.method == "POST":
        found = 0
        a = request.POST.get("t1")
        b = request.POST.get("t2")
        drec = DeptReg.objects.filter(username=a, password=b)
        if drec.filter(username=a, password=b).exists():
            found = 1
            for i in drec:
                status = i.status
                id = i.did
                panchayath = i.panchayath
                request.session['uname'] = a
                request.session['pwd'] = b
                request.session['ids'] = id
                request.session['right'] = status
                request.session['panchayath'] = panchayath
                if status == 'new department':
                    return HttpResponse('Your Application is under processing')
                elif status == 'Department':
                    form = DeptReg.objects.filter(username=request.session['uname'])
                    context={'form':form}
                    Announcement.objects.filter(expiry=datetime.now().date()).delete()
                    return redirect('/displaydept/', context)
                elif status == 'A':
                    return redirect('/adminhome/')
                else:
                    return HttpResponse('Your application is rejected')

        if found == 0:
            urec = UserReg.objects.filter(username=a, password=b)
            if urec.filter(username=a, password=b).exists():
                for i in urec:
                    id = i.uid
                    panchayath = i.panchayath
                    request.session['uname'] = a
                    request.session['pwd'] = b
                    request.session['id'] = id
                    request.session['panchayath'] = panchayath
                    Announcement.objects.filter(expiry=datetime.now().date()).delete()
                    return redirect('/display/')
            else:
                return HttpResponse("user doest exist")

    return render(request, 'login.html')


def logoutpage(request):
    return redirect('/')

def changePasswordUser(request):
    if request.method == 'POST':
        flag=0
        a = request.POST.get('t1')
        b = request.POST.get('t2')
        c = request.POST.get('t3')
        urec=UserReg.objects.filter(username=request.session['uname'], password=a)
        if urec.filter(username=request.session['uname'], password=a).exists():
            flag==1
            if b==c:
                UserReg.objects.filter(username=request.session['uname'], password=a).update(password=b)
                return redirect("/login/")
            else:
                return HttpResponse('Password miss match')
        if flag==0:
            drec=DeptReg.objects.filter(username=request.session['uname'], password=a)
            if drec.filter(username=request.session['uname'], password=a).exists():
                if b==c:
                    DeptReg.objects.filter(username=request.session['uname'], password=a).update(password=b)
                    return redirect("/login/")
                else:
                    return HttpResponse('Password miss match')
    else:
        return render(request, "changepassword.html")



def post(request):
    max_postid=Post.objects.aggregate(max_postid=Coalesce(Max('postid'), Value(0))) ['max_postid']
    pid = int(max_postid)+1
    prec = UserReg.objects.filter(username=request.session['uname'])
    if prec.filter(username=request.session['uname']).exists():


            if request.method == "POST":

                # des = request.POST.get('description')
                # photo = request.POST.get('photo')
                #
                # post = Post(creatorid=request.session['id'], creator=request.session['uname'],
                #             description=des)
                # post.save()

                # initial_dict = {
                #     "creatorid": 2,
                #     "creator": request.session['uname'],
                # }



                form = PostForm(request.POST, request.FILES)

                if form.is_valid():
                    print('form valid')
                    try:
                        form.save()
                        print('form saved')
                        return redirect('/display/')
                    except:
                        pass
                        print('form pass')



            else:
                form = PostForm(initial={'creatorid':request.session['id'],'creator':request.session['uname'], 'panchayath':request.session['panchayath']})

            return render(request, 'post.html', {'form':form})
    else:
        return HttpResponse('You are not logged in')



def postdept(request):
    pdrec = DeptReg.objects.filter(username=request.session['uname'])
    if pdrec.filter(username=request.session['uname']).exists():


            if request.method == "POST":

                # des = request.POST.get('description')
                # photo = request.POST.get('photo')
                #
                # post = Post(creatorid=request.session['id'], creator=request.session['uname'],
                #             description=des, pimage=photo)
                # post.save()

            #     form = PostForm(request.POST)
            #
                form = PostForm(request.POST, request.FILES)

                if form.is_valid():
                    print('form valid')
                    try:
                        form.save()
                        print('form saved')
                        return redirect('/displaydept/')
                    except:
                        pass
                        print('form pass')

            else:
                form = PostForm(initial={'creatorid': request.session['ids'], 'creator': request.session['uname'], 'panchayath':request.session['panchayath']})

            return render(request, 'postdept.html', {'form':form})
    else:
        return HttpResponse('You are not logged in')

def displayPost(request):
    post = Post.objects.filter(panchayath=request.session['panchayath'])
    rec = UserReg.objects.filter(username=request.session['uname'])
    p = request.session['panchayath']
    alrec = Announcement.objects.filter(panchayath=p)
    return render(request, "userhome.html", {"post":post, "alrec":alrec, "rec":rec})

def displayPostDept(request):
    post = Post.objects.filter(panchayath=request.session['panchayath'])
    rec = DeptReg.objects.filter(username=request.session['uname'])
    p = request.session['panchayath']
    alrec = Announcement.objects.filter(panchayath=p)
    return render(request, "depthome.html", {"post":post, "alrec":alrec, "rec":rec})


def delete(request,postid):
    if Post.objects.filter(creator=request.session['uname'], postid=postid):
        Post.objects.filter(creator=request.session['uname'], postid=postid).delete()
        if UserReg.objects.filter(username=request.session['uname']):
            return redirect('/display/')
        elif DeptReg.objects.filter(username=request.session['uname']):
            return redirect('/displaydept')
        else:
            return HttpResponse('you are not logged in')
    else:
        return HttpResponse('You have no permission to delete this post')


# class PostUpdate(UpdateView):
#     model = Post
#     fields = '__all__'
#     success_url = '/display/'


def update(request, postid):
    if Post.objects.filter(creator=request.session['uname'], postid=postid):
        context = {}
        obj = get_object_or_404(Post, postid=postid)
        form = PostForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            # return redirect('/display/')
            if DeptReg.objects.filter(username=request.session['uname']).exists():
                return redirect('/displaydept/')
            else:
                return redirect('/display/')

        context["form"] = form
        return render(request, "update.html", context)
    return HttpResponse('You have no permission to edit this post')



# class PostDelete(DeleteView):
#
#     model = Post
#     success_url = '/display/'


# def upvote(request, postid):
#     # like = Post.objects.geupvote)
#     # like = like + 1
#
#     uprec = Vote.objects.filter(uid=request.session['ids'], postid=postid).exists()
#     print(request.session['ids'],postid,uprec);
#     if Vote.objects.filter(uid=request.session['ids'], postid=postid).exists():
#         print("entering...");
#         for i in uprec:
#             u = i.upvotestatus
#             d = i.downvotestatus
#         print('hi hello')
#         print(d)
#         if u==1:
#             return redirect('/userhome/')
#         elif u==0 and d==0:
#             Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
#             Vote.objects.filter(postid=postid).update(upvotestatus=F('upvotestatus') + 1)
#         elif u==0 and d==1:
#             Post.objects.filter(postid=postid).update(downvote=F('downvote') - 1)
#             Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
#     else:
#         print("no user exists")
#     # Post.objects.filter(creator=request.session['uname'], creatorid=request.session['id'])
#     # Vote.objects.filter(creatorid=request.session['id']).update(upvotestatus=1)
#     return redirect('/display/')


def upvote(request, postid):
    # like = Post.objects.geupvote)
    # like = like + 1

    if UserReg.objects.filter(username=request.session['uname']).exists():

        # uprec = Vote.objects.filter(uid=request.session['id'], postid=postid)
        if  Vote.objects.filter(userid=request.session['id'], postid=postid).exists():
            print("dummy");
            if Vote.objects.filter(upvotestatus=0, downvotestatus=1,userid=request.session['id'], postid=postid):
                print("third else")
                Post.objects.filter(postid=postid).update(downvote=F('downvote') - 1)
                Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
                Vote.objects.filter(postid=postid).update(upvotestatus=F('upvotestatus')+1)
                Vote.objects.filter(postid=postid).update(downvotestatus=F('downvotestatus') - 1)
            else:
                print("display")
                return redirect('/display/')

        else:
            print("else")
            print("final else")
            Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
            vote = Vote(postid=postid,userid=request.session['id'],downvotestatus=0,upvotestatus=1)
            vote.save()


        # Post.objects.filter(creator=request.session['uname'], creatorid=request.session['id'])
        # Vote.objects.filter(creatorid=request.session['id']).update(upvotestatus=1)

    else:
        print('dept work')
        if Vote.objects.filter(username=request.session['uname'], postid=postid).exists():
            print("dummy");
            if Vote.objects.filter(upvotestatus=0, downvotestatus=1, userid=request.session['ids'], postid=postid):
                print("third else")
                Post.objects.filter(postid=postid).update(downvote=F('downvote') - 1)
                Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
                Vote.objects.filter(postid=postid).update(upvotestatus=F('upvotestatus') + 1)
                Vote.objects.filter(postid=postid).update(downvotestatus=F('downvotestatus') - 1)
            else:
                print("displaydept")
                return redirect('/displaydept/')

        else:
            print("else")
            print("final else")
            Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
            vote = Vote(postid=postid, username=request.session['uname'], downvotestatus=0, upvotestatus=1)
            vote.save()
            return redirect('/displaydept/')
    if DeptReg.objects.filter(username=request.session['uname']).exists():
        return redirect('/displaydept/')
    else:
        return redirect('/display/')


# def downvote(request, postid):
#     dnrec = Vote.objects.filter(uid=request.session['ids'], postid=postid)
#     if dnrec.filter(uid=request.session['ids'], postid=postid).exists():
#
#         for i in dnrec:
#             up = i.upvotestatus
#             dn = i.downvotestatus
#
#         if dn==1:
#             return redirect('/userhome')
#         elif up==0 and dn==0:
#             Post.objects.filter(postid=postid).update(downvote=F('downvote') + 1)
#         elif up==1 and dn==0:
#             Post.objects.filter(postid=postid).update(upvote=F('upvote') - 1)
#             Post.objects.filter(postid=postid).update(downvote=F('downvote') + 1)
#
#     # Post.objects.filter(creator=request.session['uname'], creatorid=request.session['id'])
#     # Vote.objects.filter(creatorid=request.session['id']).update(upvotestatus=1)
#     return redirect('/display/')


def downvote(request, postid):

    if UserReg.objects.filter(username=request.session['uname']).exists():

        # dnrec = Vote.objects.filter(uiserd=request.session['id'], postid=postid)
        if Vote.objects.filter(userid=request.session['id'], postid=postid).exists():
        #     dpr = Vote.objects.all()
        #     if dpr.filter(upvotestatus=0, downvotestatus=1):
        #         return redirect('/userhome/')
            if Vote.objects.filter(upvotestatus=1, downvotestatus=0,userid=request.session['id'], postid=postid):
                Post.objects.filter(postid=postid).update(upvote=F('upvote') - 1)
                Post.objects.filter(postid=postid).update(downvote=F('downvote') + 1)
                Vote.objects.filter(postid=postid).update(downvotestatus=F('downvotestatus') + 1)
                Vote.objects.filter(postid=postid).update(upvotestatus=F('upvotestatus') - 1)

            else:
                return redirect('/display/')

        else:
            Post.objects.filter(postid=postid).update(downvote=F('downvote') + 1)
            vote = Vote(postid=postid, userid=request.session['id'], downvotestatus=1, upvotestatus=0)
            vote.save()
        # Post.objects.filter(creator=request.session['uname'], creatorid=request.session['id'])
        # Vote.objects.filter(creatorid=request.session['id']).update(upvotestatus=1)

    else:
        print(' down vote dept work')
        if Vote.objects.filter(username=request.session['uname'], postid=postid).exists():
            print("down vote dummy");
            if Vote.objects.filter(upvotestatus=1, downvotestatus=0, userid=request.session['ids'], postid=postid):
                print(" down vote third else")
                Post.objects.filter(postid=postid).update(upvote=F('upvote') - 1)
                Post.objects.filter(postid=postid).update(downvote=F('downvote') + 1)
                Vote.objects.filter(postid=postid).update(downvotestatus=F('downvotestatus') + 1)
                Vote.objects.filter(postid=postid).update(upvotestatus=F('upvotestatus') - 1)
            else:
                print("displaydept")
                return redirect('/displaydept/')

        else:
            print("else")
            print(" downvote final else")
            Post.objects.filter(postid=postid).update(downvote=F('downvote') + 1)
            vote = Vote(postid=postid, username=request.session['uname'], downvotestatus=1, upvotestatus=0)
            vote.save()
            return redirect('/displaydept/')

    if DeptReg.objects.filter(username=request.session['uname']).exists():
        return redirect('/displaydept/')
    else:
        return redirect('/display/')




# def upvotedept(request, postid):
#     # like = Post.objects.geupvote)
#     # like = like + 1
#
#     uprec = Vote.objects.filter(uid=request.session['ids'], postid=postid)
#     if  Vote.objects.filter(uid=request.session['ids'], postid=postid).exists():
#         print("dummy");
#         if Vote.objects.filter(upvotestatus=0, downvotestatus=1,uid=request.session['ids'], postid=postid):
#             print("third else")
#             Post.objects.filter(postid=postid).update(downvote=F('downvote') - 1)
#             Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
#             Vote.objects.filter(postid=postid).update(upvotestatus=F('upvotestatus')+1)
#             Vote.objects.filter(postid=postid).update(downvotestatus=F('downvotestatus') - 1)
#         else:
#             print("display")
#             return redirect('/display/')
#
#     else:
#         print("else")
#         print("final else")
#         Post.objects.filter(postid=postid).update(upvote=F('upvote') + 1)
#         vote = Vote(postid=postid,uid=request.session['ids'],downvotestatus=0,upvotestatus=1)
#         vote.save()
#
#
#     # Post.objects.filter(creator=request.session['uname'], creatorid=request.session['id'])
#     # Vote.objects.filter(creatorid=request.session['id']).update(upvotestatus=1)
#     return redirect('/display/')






def neighbours(request):
    nbrec = UserReg.objects.filter(username=request.session['uname'])
    if nbrec.filter(username=request.session['uname']).exists():

        rec = UserReg.objects.filter(username=request.session['uname'])
        n = UserReg.objects.filter(panchayath=request.session['panchayath'])
        nrec = n.exclude(username=request.session['uname'])
        return render(request, 'neighbours.html', {'nrec':nrec, 'rec':rec})
    else:
        return HttpResponse('You are not logged in')


def people(request):
    nbrec = DeptReg.objects.filter(username=request.session['uname'])
    if nbrec.filter(username=request.session['uname']).exists():

        rec = UserReg.objects.filter(username=request.session['uname'])
        n = UserReg.objects.filter(panchayath=request.session['panchayath'])
        nrec = n.exclude(username=request.session['uname'])
        return render(request, 'people.html', {'nrec':nrec, 'rec':rec})
    else:
        return HttpResponse('You are not logged in')


def complaints(request):
    crec = UserReg.objects.filter(username=request.session['uname'])
    if crec.filter(username=request.session['uname']).exists():
            rec = UserReg.objects.filter(username=request.session['uname'])
            if request.method == "POST":
            # form = ComplaintForm(request.POST)
                dept = request.POST.get('department')
                complaint = request.POST.get('complaint')

                comp = Complaints(uid=request.session['id'], uname=request.session['uname'],
                                  panchayath=request.session['panchayath'], department=dept, complaint = complaint)

                comp.save()
            #     if form.is_valid():
            #         try:
            #             form.save()
            #         except:
            #             pass
            #
            # else:
            #     form = ComplaintForm

            return render(request, 'complaints.html', {'rec':rec})
    else:
        return HttpResponse('You are not logged in')


def complaintList(request):
    clrec = DeptReg.objects.filter(username=request.session['uname'])
    if clrec.filter(username=request.session['uname']).exists():
        rec = UserReg.objects.filter(username=request.session['uname'])

        crec = Complaints.objects.filter(panchayath=request.session['panchayath'])
        return render(request, 'complaintlist.html', {'crec': crec, 'rec':rec})
    else:
        return HttpResponse('You are not logged in')


def settings(request):
    if UserReg.objects.filter(username=request.session['uname']).exists():
        rec = UserReg.objects.filter(username=request.session['uname'])
        return render(request, 'settings.html' , {'rec':rec})
    else:
        return HttpResponse('you are not logged in')

def settingsdept(request):
    if DeptReg.objects.filter(username=request.session['uname']).exists():
        rec = UserReg.objects.filter(username=request.session['uname'])
        return render(request, 'settingsdept.html' , {'rec':rec})
    else:
        return HttpResponse('you are not logged in')


def profileuser(request):
    pfrec = UserReg.objects.filter(username=request.session['uname'])
    post = Post.objects.filter(creator=request.session['uname'])
    return render(request, 'profile.html', {'pfrec':pfrec, "post":post})

def profiledept(request):
    pdrec = DeptReg.objects.filter(username=request.session['uname'])
    post = Post.objects.filter(creator=request.session['uname'])
    return render(request, 'profiledept.html', {'pdrec':pdrec, "post":post})


def announcement(request):
    arec = DeptReg.objects.filter(username=request.session['uname'])
    if arec.filter(username=request.session['uname']).exists():
        if request.method == "POST":

            announcement = request.POST.get('announcement')

            anno = Announcement(uid=request.session['ids'], uname=request.session['uname'],
                              panchayath=request.session['panchayath'], department=request.session['uname'], announcement=announcement)

            anno.save()
            return redirect('/displaydept/')

        return render(request, 'announcement.html')
    else:
        return HttpResponse('You are not logged in')


def announcementlist(request):
    p = request.session['panchayath']
    alrec = Announcement.objects.filter(panchayath=p)
    return render(request, 'displaydept.html', {'alrec': alrec})



def messagepage(request):
    m = request.session['panchayath']
    ml = UserReg.objects.filter(panchayath=m)
    mlrec = ml.exclude(username=request.session['uname'])
    p = request.session['panchayath']
    alrec = Announcement.objects.filter(panchayath=p)
    rec = UserReg.objects.filter(username=request.session['uname'])
    return render(request, 'message.html', {'mlrec': mlrec, 'alrec':alrec, 'rec':rec})


def messagepost(request, uid, username):
    mprec = UserReg.objects.filter(username=request.session['uname'])
    if mprec.filter(username=request.session['uname']).exists():
        if request.method == "POST":
            a = request.POST.get('message')
            # form = MessageForm(request.POST)
            m = Message(receiverid=uid,senderid=request.session['id'] , sendername=request.session['uname'],
                        receivername=username , panchayath=request.session['panchayath'], message=a)
            m.save()
            # if form.is_valid():
            #     try:
            #         form.save()
            #         return redirect('/message/')
            #     except:
            #         pass

        # else:
        #     form = MessageForm
        mr = Message.objects.filter(senderid=uid, receiverid=request.session['id'] )
        ms = Message.objects.filter(receiverid=uid, senderid=request.session['id'])
        m = request.session['panchayath']
        ml = UserReg.objects.filter(panchayath=m)
        mlrec = ml.exclude(username=request.session['uname'])
        return render(request, 'messagepost.html', {'mr':mr, 'ms':ms, 'mlrec': mlrec})
    else:
        return HttpResponse('You are not logged in')



# def messagereceive(request):
#     mr = Message.objects.filter(senderid=uid, receiverid=request.session['id'])
#     return render(request, 'messagepost.html', {'mr':mr})


def comments(request,postid):
    post = Post.objects.get(postid=postid)

    commentator = request.session['uname']
    comments = Comments.objects.filter(postid=postid)

    if request.method == "POST":
        a = request.POST.get('message')

        crec = Comments(comment=a, commentator=commentator, commentatorid=request.session['id'], postid=postid)
        crec.save()
        Post.objects.filter(postid=postid).update(commentcount=F('commentcount') + 1)


    p = request.session['panchayath']
    alrec = Announcement.objects.filter(panchayath=p)
    return render(request, "comments.html", {"post":post, "alrec":alrec, "comments":comments})


def deleteComment(request, commentid, postid):
    if Comments.objects.filter(commentator=request.session['uname'], commentid=commentid):
        Comments.objects.filter(commentator=request.session['uname'], commentid=commentid).delete()
        Post.objects.filter(postid=postid).update(commentcount=F('commentcount') - 1)
        return redirect('comments',postid)
    else:
        return HttpResponse('You have no permission to delete this post')



class Editprofile(UpdateView):
    model = UserReg
    fields = '__all__'
    success_url = '/profile'

class EditprofileDept(UpdateView):
    model = DeptReg
    fields = '__all__'
    success_url = '/profiledept'


def peopleProfile(request, username):
    if UserReg.objects.filter(username=username).exists():
        pprec = UserReg.objects.filter(username=username)
        post = Post.objects.filter(creator=username)
        return render(request, 'peopleprofile.html',{'pprec':pprec, 'post':post})
    else:
        pprec = DeptReg.objects.filter(username=username)
        post = Post.objects.filter(creator=username)
        return render(request, 'peopleprofile.html',{'pprec':pprec, 'post':post})

    return render(request, 'peopleprofile.html')


def searchbar(request):
    if request.method =='GET':
        search=request.GET.get('search')
        if Post.objects.all().filter(creator=search):
            post=Post.objects.all().filter(creator=search)
            return render(request,'search.html',{'post':post})
        else:
            return HttpResponse('No result found')

def searchbardept(request):
    if request.method =='GET':
        search=request.GET.get('search')
        if Post.objects.all().filter(creator=search):
            post=Post.objects.all().filter(creator=search)
            return render(request,'searchdept.html',{'post':post})
        else:
            return HttpResponse('No result found')


def adminhome(request):
    return render(request, 'adminhome.html')