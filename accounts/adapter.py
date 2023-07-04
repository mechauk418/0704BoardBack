from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user = super().save_user(request,user,form,False)
        nickname = data.get('nickname')
        realname = data.get('realname')
        if nickname:
            user.nickname = nickname
        if realname:
            user.realname = realname
        user.save()
        return super().save_user(request, user, form, commit)