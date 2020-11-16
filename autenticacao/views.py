# Create your views here.

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Users

import cv2
import fingerprint_enhancer


username = ''
autenticado = False

def autenticacao(request):
    if request.method == "POST":
        try:
            uploaded_file = request.FILES['biometry']
            fs = FileSystemStorage()
            fs.save("fingerprint.png", uploaded_file)
        except:
            return redirect('home/')

        global username
        username = request.POST['username']

        try:
            Users.objects.filter(username=username).first().username
            print("Username cadastrado no BD")
            try:
                print('Analisando o fingerprint recebido')
                img = cv2.imread('./upload/fingerprint.png',
                                 0)						# read input image
                out = fingerprint_enhancer.enhance_Fingerprint(
                    img)		# enhance the fingerprint image

                print('Analisando o fingerprint cadastrado no BD')
                img2 = cv2.imread('./upload/' + Users.objects.filter(
                    username=username).first().biometry.name, 0)   # read input image
                out2 = fingerprint_enhancer.enhance_Fingerprint(
                    img2)		# enhance the fingerprint image

                result = out == out2

                try:
                    global autenticado
                    if result.all() == True:
                        autenticado = True
                        print("Autenticado!")
                        fs.delete("fingerprint.png")
                        return redirect('home/')
                except:
                    if result == False:
                        autenticado = False
                        print("Falha na autenticação!")
                        fs.delete("fingerprint.png")
                        return redirect('home/')

            except:
                print("Obtivemos um erro ao analisarmos a fingerprint recebida. Por favor, verifique se a fingerprint está no formato JPEG, JPG ou PNG.")
                fs.delete("fingerprint.png")
                return redirect('home/')
        except:
            print("Usuario não cadastrado no BD")
            fs.delete("fingerprint.png")
            return redirect('home/')

    return render(request, 'auth/src/auth.html')


def home(request):
    data = {}
    try:
        data['accessLevel'] = Users.objects.filter(
            username=username).first().accessLevel
        data['username'] = Users.objects.filter(
            username=username).first().username
        data['autenticado'] = autenticado
        return render(request, 'home/index.html', data)
    except:
        data['autenticado'] = False
        return render(request, 'home/index.html', data)
