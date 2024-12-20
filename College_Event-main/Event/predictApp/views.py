from django.shortcuts import render
from joblib import load

model = load('../SavedModels/model.joblib')
# Create your views here.
def predictor(request):
    if request.method == "POST":
        sepal_length = request.POST['sepal_length']
        sepal_width = request.POST['sepal_length']
        pedal_length = request.POST['sepal_length']
        pedal_width = request.POST['sepal_length']
        y_pred = model.predict([[sepal_length,sepal_width,pedal_length,pedal_width]])
        print(y_pred)

        if y_pred[0] == 0:
            y_pred = "Setosa"
        elif y_pred[0] == 1:
            y_pred = "verscicolor"
        else:
            y_pred = "Virginica"

        return render(request,'main.html',{'result': y_pred})

    return render(request,'main.html')





# we don't use it below code.
# def formInfo(request):
#     sepal_length = request.GET['sepal_length']
#     sepal_width = request.GET['sepal_length']
#     pedal_length = request.GET['sepal_length']
#     pedal_width = request.GET['sepal_length']
#     y_pred = model.predict([[sepal_length,sepal_width,pedal_length,pedal_width]])
#     print(y_pred)

#     if y_pred[0] == 0:
#         y_pred = "Setosa"
#     elif y_pred[0] == 1:
#         y_pred = "verscicolor"
#     else:
#         y_pred = "Virginica"
#     return render(request,'result.html',{'result': y_pred})