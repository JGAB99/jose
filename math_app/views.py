from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Sum, Q
from .models import User, Exercise, Achievement, UserAchievement, Tutorial
from .forms import UserRegisterForm, ExerciseForm
from .models import Tutorial
import random
import math
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home') 


def home(request):
    return render(request, 'math_app/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'math_app/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    achievements = UserAchievement.objects.filter(user=user)
    return render(request, 'math_app/dashboard.html', {'user': user, 'achievements': achievements})






@login_required
def exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = Exercise.objects.get(id=request.POST.get('exercise_id'))
            exercise.user_answer = form.cleaned_data['user_answer']
            exercise.is_correct = abs(float(exercise.user_answer) - float(exercise.correct_answer)) < 0.01
            exercise.user = request.user
            exercise.save()
            
            if exercise.is_correct:
                old_level = request.user.level
                request.user.experience += 10 * exercise.difficulty
                if request.user.experience >= request.user.level * 100:
                    request.user.level += 1
                    request.user.experience = 0
                request.user.save()
                
                new_achievements = check_achievements(request.user)
                if new_achievements:
                    messages.success(request, f"¡Has desbloqueado {len(new_achievements)} nuevo(s) logro(s)!")
                if old_level != request.user.level:
                    messages.success(request, f"¡Has subido al nivel {request.user.level}!")
                    return redirect('dashboard')
            
            return render(request, 'math_app/exercise_result.html', {'exercise': exercise})
    else:
        exercise = generate_exercise(request.user.level)
        form = ExerciseForm()
    
    return render(request, 'math_app/exercise.html', {'form': form, 'exercise': exercise})

@login_required
def practice_mode(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise_id = request.POST.get('exercise_id')
            if exercise_id:
                try:
                    exercise = Exercise.objects.get(id=exercise_id)
                except Exercise.DoesNotExist:
                    exercise = None
            else:
                exercise = None

            if exercise is None:
                exercise = generate_exercise(request.user.level)
                exercise.user = request.user
                exercise.save()

            exercise.user_answer = form.cleaned_data['user_answer']
            exercise.is_correct = abs(float(exercise.user_answer) - float(exercise.correct_answer)) < 0.01
            exercise.save()
            
            return render(request, 'math_app/practice_result.html', {
                'exercise': exercise,
            })
    else:
        exercise = generate_exercise(request.user.level)
        exercise.user = request.user
        exercise.save()
        form = ExerciseForm()
    
    return render(request, 'math_app/practice_mode.html', {'form': form, 'exercise': exercise})




@login_required
def leaderboard(request):
    leaders = User.objects.annotate(
        total_score=Sum('exercise__difficulty', filter=Q(exercise__is_correct=True))
    ).order_by('-level', '-experience', '-total_score')[:10]
    return render(request, 'math_app/leaderboard.html', {'leaders': leaders})

 

def tutorial_list(request):
    tutorials = Tutorial.objects.all()
    return render(request, 'math_app/tutorial_list.html', {'tutorials': tutorials})

@login_required
def tutorial_detail(request, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    return render(request, 'math_app/tutorial_detail.html', {'tutorial': tutorial})

def generate_exercise(user_level):
    difficulty = min(user_level, 5)
    exercise_type = random.choice([choice[0] for choice in Exercise.TYPES])
    
    if exercise_type == 'addition':
        a = random.randint(1, 10 * difficulty)
        b = random.randint(1, 10 * difficulty)
        question = f"{a} + {b}"
        answer = a + b
        explanation = f"Paso 1: Identifica los números a sumar: {a} y {b}.\n"
        explanation += f"Paso 2: Suma los números: {a} + {b} = {answer}.\n"
        explanation += "Paso 3: El resultado es la suma total."

    elif exercise_type == 'subtraction':
        a = random.randint(1, 10 * difficulty)
        b = random.randint(1, a)
        question = f"{a} - {b}"
        answer = a - b
        explanation = f"Paso 1: Identifica el número mayor ({a}) y el número a restar ({b}).\n"
        explanation += f"Paso 2: Resta el número menor del mayor: {a} - {b} = {answer}.\n"
        explanation += "Paso 3: El resultado es la diferencia entre los dos números."

    elif exercise_type == 'multiplication':
        a = random.randint(1, 5 * difficulty)
        b = random.randint(1, 5 * difficulty)
        question = f"{a} × {b}"
        answer = a * b
        explanation = f"Paso 1: Identifica los números a multiplicar: {a} y {b}.\n"
        explanation += f"Paso 2: Multiplica los números: {a} × {b} = {answer}.\n"
        explanation += "Paso 3: El resultado es el producto de los dos números."

    elif exercise_type == 'division':
        b = random.randint(1, 5 * difficulty)
        a = b * random.randint(1, 5 * difficulty)
        question = f"{a} ÷ {b}"
        answer = a / b
        explanation = f"Paso 1: Identifica el dividendo ({a}) y el divisor ({b}).\n"
        explanation += f"Paso 2: Divide el dividendo entre el divisor: {a} ÷ {b} = {answer}.\n"
        explanation += "Paso 3: El resultado es el cociente de la división."

    elif exercise_type == 'exponentiation':
        a = random.randint(2, 2 + difficulty)
        b = random.randint(2, 2 + difficulty)
        question = f"{a}^{b}"
        answer = a ** b
        explanation = f"Paso 1: Identifica la base ({a}) y el exponente ({b}).\n"
        explanation += f"Paso 2: Multiplica la base por sí misma {b} veces: {a} × {a} × ... ({b} veces) = {answer}.\n"
        explanation += "Paso 3: El resultado es el valor de la base elevada al exponente."

    elif exercise_type == 'root':
        a = random.randint(2, 5 * difficulty) ** 2
        question = f"√{a}"
        answer = math.sqrt(a)
        explanation = f"Paso 1: Identifica el número bajo la raíz cuadrada: {a}.\n"
        explanation += f"Paso 2: Encuentra el número que, multiplicado por sí mismo, da {a}.\n"
        explanation += f"Paso 3: La raíz cuadrada de {a} es {answer}, porque {answer} × {answer} = {a}."

    elif exercise_type == 'logarithm':
        b = random.randint(2, 2 + difficulty)
        a = b ** random.randint(2, 2 + difficulty)
        question = f"log_{b}({a})"
        answer = math.log(a, b)
        explanation = f"Paso 1: Identifica la base del logaritmo ({b}) y el número ({a}).\n"
        explanation += f"Paso 2: Encuentra el exponente al que hay que elevar {b} para obtener {a}.\n"
        explanation += f"Paso 3: log_{b}({a}) = {answer}, porque {b}^{answer} = {a}."

    else:  # trigonometry
        angle = random.choice([30, 45, 60, 90, 180, 270, 360])
        function = random.choice(['sin', 'cos', 'tan'])
        question = f"{function}({angle}°)"
        if function == 'sin':
            answer = math.sin(math.radians(angle))
            explanation = f"Paso 1: Convierte el ángulo de grados a radianes: {angle}° × (π/180) = {math.radians(angle)} radianes.\n"
            explanation += f"Paso 2: Calcula el seno de {math.radians(angle)} radianes.\n"
            explanation += f"Paso 3: El resultado es {answer}."
        elif function == 'cos':
            answer = math.cos(math.radians(angle))
            explanation = f"Paso 1: Convierte el ángulo de grados a radianes: {angle}° × (π/180) = {math.radians(angle)} radianes.\n"
            explanation += f"Paso 2: Calcula el coseno de {math.radians(angle)} radianes.\n"
            explanation += f"Paso 3: El resultado es {answer}."
        else:
            answer = math.tan(math.radians(angle))
            explanation = f"Paso 1: Convierte el ángulo de grados a radianes: {angle}° × (π/180) = {math.radians(angle)} radianes.\n"
            explanation += f"Paso 2: Calcula la tangente de {math.radians(angle)} radianes.\n"
            explanation += f"Paso 3: El resultado es {answer}."

    return Exercise.objects.create(
        type=exercise_type,
        difficulty=difficulty,
        question=question,
        correct_answer=round(answer, 2),
        explanation=explanation
    )
   


def check_achievements(user):
    achievements = []
    
    # Logros existentes
    if user.exercise_set.filter(is_correct=True).count() == 1:
        achievement, created = Achievement.objects.get_or_create(
            name="Primer Paso",
            defaults={"description": "Completaste tu primer ejercicio correctamente", "icon": "fa-solid fa-shoe-prints"}
        )
        user_achievement, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
        if created:
            achievements.append(achievement)
    
    if user.exercise_set.filter(is_correct=True).count() == 10:
        achievement, created = Achievement.objects.get_or_create(
            name="Aprendiz Dedicado",
            defaults={"description": "Completaste 10 ejercicios correctamente", "icon": "fa-solid fa-star"}
        )
        user_achievement, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
        if created:
            achievements.append(achievement)
    
    # Nuevos logros por nivel
    level_achievements = [
        {"level": 2, "name": "Novato Prometedor", "description": "Alcanzaste el nivel 2", "icon": "fa-solid fa-seedling"},
        {"level": 3, "name": "Estudiante Aplicado", "description": "Alcanzaste el nivel 3", "icon": "fa-solid fa-book-open"},
        {"level": 4, "name": "Matemático Aficionado", "description": "Alcanzaste el nivel 4", "icon": "fa-solid fa-square-root-variable"},
        {"level": 5, "name": "Matemático en Progreso", "description": "Alcanzaste el nivel 5", "icon": "fa-solid fa-chart-line"},
        {"level": 10, "name": "Maestro de los Números", "description": "Alcanzaste el nivel 10", "icon": "fa-solid fa-crown"},
        {"level": 15, "name": "Genio Matemático", "description": "Alcanzaste el nivel 15", "icon": "fa-solid fa-brain"},
        {"level": 20, "name": "Leyenda de las Matemáticas", "description": "Alcanzaste el nivel 20", "icon": "fa-solid fa-trophy"},
    ]

    for achievement_data in level_achievements:
        if user.level >= achievement_data["level"]:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data["name"],
                defaults={
                    "description": achievement_data["description"],
                    "icon": achievement_data["icon"],
                    "level_required": achievement_data["level"]
                }
            )
            user_achievement, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
            if created:
                achievements.append(achievement)

    return achievements



def tutorial_detail(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    return render(request, 'math_app/tutorial_detail.html', {'tutorial': tutorial})



 